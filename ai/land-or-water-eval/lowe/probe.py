"""Model probes.

A probe answers "land or water?" for a list of (lat, lon) and returns a list
of "L" / "W" strings, aligned with the input order.

Backends
  mock      -- always answers "land" (the degenerate baseline in the tweet)
  file      -- reads a cached prediction written by an earlier run
  openai    -- any OpenAI-compatible /v1/chat/completions endpoint
  anthropic -- Anthropic native /v1/messages endpoint
"""

import json
import os
import re
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SYSTEM = (
    "You are a geography oracle. You are given WGS84 coordinates and must say "
    "whether the point falls on land or on water.\n"
    "Answer L for land, W for water. Water includes ocean, sea, gulf, bay, "
    "strait and large lakes. Ice sheets and ice shelves count as land.\n"
    "Reply with ONLY the letters, in the given order, separated by nothing."
)


def _fmt(lat, lon):
    return f"{abs(lat):.1f}{'N' if lat >= 0 else 'S'}, {abs(lon):.1f}{'E' if lon >= 0 else 'W'}"


def build_prompt(coords):
    body = "\n".join(f"{i + 1}) {_fmt(la, lo)}" for i, (la, lo) in enumerate(coords))
    return f"{SYSTEM}\n\nCoordinates:\n{body}\n\nAnswer ({len(coords)} letters):"


_ANSWER_RE = re.compile(r"[LW]")


def parse_answers(text, n):
    """Extract n L/W answers from a model reply. Order is preserved."""
    text = text.strip()
    for candidate in (text,):
        m = re.search(r"\[[^\]]*\]", candidate, re.S)
        if m:
            try:
                arr = json.loads(m.group(0))
                if isinstance(arr, list) and len(arr) >= n:
                    vals = [str(x).strip().upper()[:1] for x in arr[:n]]
                    if all(v in "LW" for v in vals):
                        return vals
            except Exception:
                pass
    up = text.upper()
    hits = _ANSWER_RE.findall(up)
    if len(hits) >= n:
        return hits[:n]
    # tolerate "LAND"/"WATER" spelled out
    words = re.findall(r"\b(LAND|WATER)\b", up)
    if len(words) >= n:
        return ["L" if w == "LAND" else "W" for w in words[:n]]
    return None


class MockProbe:
    """Always answers land."""

    name = "mock-always-land"

    def predict(self, coords):
        return ["L"] * len(coords)


class FileProbe:
    """Replay a cached prediction file.

    Accepted formats:
      {"predictions": ["L","W", ...]}            row-major over the grid
      {"grid": {"88": [[-100,-64], ...], ...}}   per-latitude land intervals
      raw list of "L"/"W" strings
    """

    name = "file"

    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)
        self.intervals = None
        if isinstance(self.data, dict) and isinstance(self.data.get("grid"), dict):
            self.intervals = {float(k): v for k, v in self.data["grid"].items()}

    def predict(self, coords):
        if isinstance(self.data, list):
            vals = [str(x).strip().upper()[:1] for x in self.data]
            if len(vals) != len(coords):
                raise ValueError(f"cached list has {len(vals)} entries, grid has {len(coords)}")
            return vals
        if isinstance(self.data, dict) and isinstance(self.data.get("predictions"), list):
            vals = [str(x).strip().upper()[:1] for x in self.data["predictions"]]
            if len(vals) != len(coords):
                raise ValueError(f"cached list has {len(vals)} entries, grid has {len(coords)}")
            return vals
        if self.intervals is None:
            raise ValueError("unrecognised prediction file format")
        out = []
        for lat, lon in coords:
            land = False
            for a, b in self.intervals.get(round(lat, 6), []):
                lo, hi = (a, b) if a <= b else (b, a)
                if lo <= lon <= hi:
                    land = True
                    break
            out.append("L" if land else "W")
        return out


class _HttpProbe:
    def __init__(self, model, batch=40, workers=8, temperature=0.0, max_tokens=None):
        self.model = model
        self.batch = batch
        self.workers = workers
        self.temperature = temperature
        self.max_tokens = max_tokens or batch * 4 + 32

    def _one(self, chunk):
        raise NotImplementedError

    def predict(self, coords):
        chunks = [coords[i:i + self.batch] for i in range(0, len(coords), self.batch)]
        results = [None] * len(chunks)

        def work(idx_chunk):
            idx, chunk = idx_chunk
            for attempt in range(4):
                try:
                    vals = self._one(chunk)
                    if vals and len(vals) == len(chunk):
                        return idx, vals
                except Exception:
                    pass
            return idx, None

        with ThreadPoolExecutor(max_workers=self.workers) as ex:
            for idx, vals in ex.map(work, list(enumerate(chunks))):
                results[idx] = vals

        flat, failed = [], 0
        for i, vals in enumerate(results):
            if vals is None:
                flat.extend(["L"] * len(chunks[i]))
                failed += len(chunks[i])
            else:
                flat.extend(vals)
        if failed:
            print(f"  ! {failed} points unparseable, defaulted to L")
        return flat

    @staticmethod
    def _post(url, headers, payload, timeout=120):
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode(), headers=headers, method="POST"
        )
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())


class OpenAIProbe(_HttpProbe):
    """Any OpenAI-compatible chat completions endpoint."""

    def __init__(self, model=None, base_url=None, api_key=None, **kw):
        super().__init__(model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini"), **kw)
        self.base_url = (base_url or os.environ.get("OPENAI_BASE_URL")
                         or "https://api.openai.com/v1").rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        self.name = f"openai:{self.model}"

    def _one(self, chunk):
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": build_prompt(chunk)}],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
        }
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        data = self._post(f"{self.base_url}/chat/completions", headers, payload)
        return parse_answers(data["choices"][0]["message"]["content"], len(chunk))


class AnthropicProbe(_HttpProbe):
    """Anthropic native messages API."""

    def __init__(self, model=None, api_key=None, **kw):
        super().__init__(model or os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"), **kw)
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.name = f"anthropic:{self.model}"

    def _one(self, chunk):
        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "system": SYSTEM,
            "messages": [{"role": "user", "content": build_prompt(chunk)}],
        }
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key or "",
            "anthropic-version": "2023-06-01",
        }
        data = self._post("https://api.anthropic.com/v1/messages", headers, payload)
        text = "".join(b.get("text", "") for b in data.get("content", []))
        return parse_answers(text, len(chunk))


def make_probe(kind, **kw):
    kind = kind.lower()
    if kind == "mock":
        return MockProbe()
    if kind == "file":
        return FileProbe(kw["path"])
    if kind == "openai":
        return OpenAIProbe(**kw)
    if kind == "anthropic":
        return AnthropicProbe(**kw)
    raise ValueError(f"unknown probe: {kind}")
