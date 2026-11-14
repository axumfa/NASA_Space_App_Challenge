"""Get MODIS NDVI + SMAP point samples for the demo fields from the AppEEARS API into data/raw/.

  verify    check product/layer names against the public product API (no login)
  submit    log in (credentials from .env, never printed), submit the task, remember its id
  status    show the remembered task's status
  download  download the finished task's CSVs into data/raw/
  wait      poll the REMEMBERED task until done, then download (never submits)
  run       submit (unless a task is remembered) -> poll until done -> download
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from fieldshift.fetch import appeears_api as A  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["verify", "submit", "status", "download", "wait", "run"])
    ap.add_argument("--poll-seconds", type=int, default=60)
    ap.add_argument("--logout", action="store_true", help="log out at the end (off by default: it can invalidate other sessions)")
    a = ap.parse_args()
    if a.cmd == "verify":
        bad = A.verify_layers()
        print("all products and layers verified" if not bad else f"PROBLEMS: {bad}")
        return 1 if bad else 0
    try:
        client = A.Client(A.load_credentials())
    except A.CredentialsMissing as e:
        print(f"cannot log in: {e}")
        return 2
    client.login()
    try:
        task_id = A.load_state()
        if a.cmd in ("submit", "run") and (a.cmd == "submit" or not task_id):
            bad = A.verify_layers()
            if bad:
                print(f"refusing to submit, layer check failed: {bad}")
                return 1
            task_id = client.submit(A.build_task())
            A.save_state(task_id)
            print("submitted task", task_id)
        if not task_id:
            print("no remembered task; run `submit` first")
            return 1
        if a.cmd == "status":
            print(client.status(task_id))
        if a.cmd in ("run", "wait"):
            print("final status:", client.wait(task_id, a.poll_seconds, log=lambda m: print(m, flush=True)), flush=True)
        if a.cmd in ("download", "run", "wait"):
            files = client.download(task_id)
            print("saved:", [f.name for f in files] or "nothing (task not finished?)")
    finally:
        if a.logout:
            client.logout()
    return 0


if __name__ == "__main__":
    sys.exit(main())
