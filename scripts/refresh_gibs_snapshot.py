"""Re-read the NASA GIBS metadata used by the map and store it as the committed snapshot (data/demo_cache/gibs_layers.json).

The app loads this snapshot instantly and refreshes the live copy in the background, so a fresh visitor never waits for the
6 MB capabilities file. Run this before a release so the snapshot's dates are recent; commit the result.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from fieldshift.fetch import gibs  # noqa: E402

path = Path(gibs.SNAPSHOT_DIR) / gibs.FILE
out = gibs.refresh(path=path)
bad = {k: v.reason for k, v in out.items() if not v.ok}
if bad:
    sys.exit(f"not written for: {bad}")
for k, v in out.items():
    print(f"{k:7s} {v.layer_id:45s} {v.date} {v.tms} legend={'yes' if v.legend else 'NO'}")
print(f"wrote {path} ({path.stat().st_size} bytes), fetched {json.loads(path.read_text())['fetched']:.0f}")
