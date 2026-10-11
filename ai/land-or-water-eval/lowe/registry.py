"""Model registry: resolves models.json entries into runnable probes.

A model is only runnable when its credential is present. Missing credentials
produce a skip with a reason -- never a synthetic prediction.
"""

import json
import os

from lowe.probe import AnthropicProbe, FileProbe, MockProbe, OpenAIProbe


def load_registry(path):
    with open(path) as f:
        return json.load(f)["models"]


def resolve(entry, here, batch=40, workers=8):
    """Return (probe_or_None, reason_or_None, label, mode)."""
    label = entry.get("label") or entry["id"]
    mode = entry.get("mode", "api")
    kind = entry["probe"]

    if kind == "mock":
        return MockProbe(), None, label, mode
    if kind == "file":
        p = os.path.join(here, entry["path"])
        if not os.path.exists(p):
            return None, f"prediction file missing: {entry['path']}", label, mode
        return FileProbe(p), None, label, mode

    if kind == "openai":
        key_env = entry.get("api_key_env")
        url = entry.get("base_url") or os.environ.get(entry.get("base_url_env", ""), "")
        if key_env:
            key = os.environ.get(key_env)
            if not key:
                return None, f"no credential: export {key_env}=...", label, mode
        else:
            key = None
            if not url:
                return None, "no base_url and no api_key_env", label, mode
        if not url:
            url = "https://api.openai.com/v1"
        return (OpenAIProbe(model=entry["model"], base_url=url, api_key=key,
                            batch=batch, workers=workers), None, label, mode)

    if kind == "anthropic":
        key = os.environ.get(entry.get("api_key_env", "ANTHROPIC_API_KEY"))
        if not key:
            return None, f"no credential: set {entry.get('api_key_env', 'ANTHROPIC_API_KEY')}", label, mode
        return (AnthropicProbe(model=entry["model"], api_key=key,
                               batch=batch, workers=workers), None, label, mode)

    return None, f"unknown probe {kind}", label, mode
