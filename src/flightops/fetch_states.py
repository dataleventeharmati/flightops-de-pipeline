import json
from datetime import datetime, timezone
from pathlib import Path

import requests

OPENSKY_STATES_URL = "https://opensky-network.org/api/states/all"


def main() -> None:
    # GLOBAL MODE: no bbox params -> worldwide states
    r = requests.get(OPENSKY_STATES_URL, timeout=30)
    r.raise_for_status()
    payload = r.json()

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    out_dir = Path("data/raw")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"states_{ts}_global.json"

    out_path.write_text(json.dumps(payload), encoding="utf-8")

    n_states = len(payload.get("states") or [])
    print(f"Saved: {out_path}")
    print(f"States: {n_states}")


if __name__ == "__main__":
    main()
