# File: cli/cmesh_replay.py

import argparse
import json
import os
from typing import List, Dict
from datetime import datetime

def load_memory(filepath: str) -> List[Dict]:
    if not os.path.exists(filepath):
        print(f"[!] Memory file not found: {filepath}")
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def replay_events(events: List[Dict], limit: int = 10, tag: str = None):
    filtered = []
    for event in events:
        if tag and tag not in event.get("tags", []):
            continue
        filtered.append(event)

    if not filtered:
        print(f"[!] No events found matching tag '{tag}'")
        return

    print(f"\n[🧠] Replaying {min(len(filtered), limit)} event(s):\n")
    for event in filtered[:limit]:
        ts = datetime.fromtimestamp(event["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"🔸 {ts} — {event['event_type']}")
        print(json.dumps(event["data"], indent=2))
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Replay memory events from the CerebroMesh memory mesh.")
    parser.add_argument("--file", type=str, default="mesh_data/mesh_memory.json", help="Path to the memory file")
    parser.add_argument("--tag", type=str, help="Filter events by tag")
    parser.add_argument("--limit", type=int, default=10, help="Limit number of events to replay")

    args = parser.parse_args()
    events = load_memory(args.file)
    replay_events(events, args.limit, args.tag)

if __name__ == "__main__":
    main()
