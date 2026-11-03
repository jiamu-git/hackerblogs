#!/usr/bin/env python3
"""Download open-index/hacker-news with 8 workers, watchdog + retry.

hf download resumes partial files, so a stalled attempt is killed and retried.
Progress is written to hacker-news/_progress.txt for polling.
"""
import json
import os
import shutil
import subprocess
import signal
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "hacker-news")
HF = os.path.join(ROOT, ".venv-hf", "bin", "hf")
PROGRESS = os.path.join(DEST, "_progress.txt")
MANIFEST = json.load(open(os.path.join(ROOT, "_hn_tree.json")))
FILES = [x for x in MANIFEST if x["path"].startswith("data/") and x["path"].endswith(".parquet")]
TOTAL_BYTES = sum(x["size"] for x in FILES)
WORKERS = 8
ATTEMPT_TIMEOUT = 480  # kill a stalled attempt after 8 min of no growth


def bytes_on_disk():
    n = 0
    for r, _, fs in os.walk(DEST):
        for f in fs:
            try:
                n += os.path.getsize(os.path.join(r, f))
            except OSError:
                pass
    return n


def complete_count():
    n = 0
    for x in FILES:
        p = os.path.join(DEST, x["path"])
        if os.path.exists(p) and os.path.getsize(p) == x["size"]:
            n += 1
    return n


def log(msg):
    line = f"{time.strftime('%Y-%m-%d %H:%M:%S')} {msg}"
    print(line, flush=True)
    os.makedirs(DEST, exist_ok=True)
    with open(PROGRESS, "a") as fh:
        fh.write(line + "\n")


def write_status(state, attempt):
    done = complete_count()
    got = bytes_on_disk()
    with open(PROGRESS, "a") as fh:
        fh.write(
            f"STATUS state={state} files={done}/{len(FILES)} "
            f"bytes={got} total={TOTAL_BYTES} pct={got / TOTAL_BYTES * 100:.1f} "
            f"attempt={attempt} ts={int(time.time())}\n"
        )


def run_attempt(attempt):
    env = dict(os.environ)
    env.pop("all_proxy", None)
    env.pop("ALL_PROXY", None)
    env["HF_XET_HIGH_PERFORMANCE"] = "1"
    cmd = [
        HF, "download", "open-index/hacker-news",
        "--repo-type", "dataset",
        "--include", "data/*",
        "--max-workers", str(WORKERS),
        "--local-dir", DEST,
    ]
    log(f"START attempt={attempt} workers={WORKERS}")
    p = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    last = bytes_on_disk()
    last_change = time.time()
    try:
        while p.poll() is None:
            time.sleep(10)
            now = bytes_on_disk()
            if now > last:
                last = now
                last_change = time.time()
            if time.time() - last_change > ATTEMPT_TIMEOUT:
                log(f"STALL detected (no growth {ATTEMPT_TIMEOUT}s), killing attempt={attempt}")
                p.send_signal(signal.SIGTERM)
                try:
                    p.wait(20)
                except subprocess.TimeoutExpired:
                    p.kill()
                return "stalled"
            if complete_count() >= len(FILES):
                break
        if complete_count() >= len(FILES):
            try:
                p.wait(30)
            except subprocess.TimeoutExpired:
                p.kill()
            return "done"
        return f"exit:{p.returncode}"
    finally:
        if p.poll() is None:
            p.kill()


def main():
    os.makedirs(DEST, exist_ok=True)
    log(f"BEGIN files={len(FILES)} total={TOTAL_BYTES / 1e9:.2f}GB dest={DEST}")
    for attempt in range(1, 41):
        if complete_count() >= len(FILES):
            break
        t0 = time.time()
        r = run_attempt(attempt)
        write_status(r, attempt)
        log(f"END attempt={attempt} result={r} elapsed={time.time() - t0:.0f}s")
        if r == "done":
            break
        time.sleep(5)
    done = complete_count()
    got = bytes_on_disk()
    log(f"FINISH files={done}/{len(FILES)} bytes={got} ({got / 1e9:.2f}GB)")
    write_status("finished", 0)


if __name__ == "__main__":
    main()
