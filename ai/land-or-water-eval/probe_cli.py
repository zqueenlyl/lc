#!/usr/bin/env python3
"""Hard-timeout probe for the bundled codebuddy CLI headless mode."""
import os
import subprocess
import sys
import time

CBC = "/Applications/WorkBuddy.app/Contents/Resources/app.asar.unpacked/cli/bin/codebuddy"

def probe(args, timeout=100, label=""):
    print(f"\n===== {label} :: {' '.join(args[:6])} ... =====", flush=True)
    env = dict(os.environ)
    env["CI"] = "1"
    t0 = time.time()
    try:
        p = subprocess.run([CBC] + args, cwd="/tmp/lowq", capture_output=True,
                           text=True, timeout=timeout, env=env,
                           stdin=subprocess.DEVNULL)
        dt = time.time() - t0
        print(f"rc={p.returncode} in {dt:.1f}s", flush=True)
        print("-- stdout --", flush=True)
        print(p.stdout[-3000:], flush=True)
        print("-- stderr --", flush=True)
        print(p.stderr[-3000:], flush=True)
    except subprocess.TimeoutExpired as e:
        print(f"TIMEOUT after {timeout}s", flush=True)
        out = e.stdout or b""
        err = e.stderr or b""
        if isinstance(out, bytes):
            out = out.decode(errors="replace")
        if isinstance(err, bytes):
            err = err.decode(errors="replace")
        print("-- partial stdout --", flush=True)
        print(out[-3000:], flush=True)
        print("-- partial stderr --", flush=True)
        print(err[-3000:], flush=True)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "plain"):
        probe(["-p", "Reply with exactly: OK"], label="plain no model")
    if which in ("all", "model"):
        probe(["-p", "--model", "hy3-ioa", "Reply with exactly: OK"], label="with model")
    if which in ("all", "debug"):
        probe(["-p", "-d", "--model", "hy3-ioa", "Reply with exactly: OK"], label="debug")
