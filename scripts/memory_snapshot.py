# File: scripts/memory_snapshot.py

import json
import os
from datetime import datetime
from typing import List, Dict

class MemorySnapshot:
    def __init__(self, memory_path: str = "mesh_data/mesh_memory.json", snapshot_dir: str = "mesh_data/snapshots"):
        self.memory_path = memory_path
        self.snapshot_dir = snapshot_dir
        self.snapshot_data: List[Dict] = []

    def load_memory(self) -> List[Dict]:
        if not os.path.exists(self.memory_path):
            print(f"[!] Memory file not found: {self.memory_path}")
            return []
        with open(self.memory_path, "r") as f:
            return json.load(f)

    def create_snapshot(self) -> str:
        self.snapshot_data = self.load_memory()
        if not self.snapshot_data:
            print("[!] No memory events to snapshot.")
            return ""

        os.makedirs(self.snapshot_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        snapshot_file = os.path.join(self.snapshot_dir, f"snapshot_{timestamp}.json")

        with open(snapshot_file, "w") as f:
            json.dump(self.snapshot_data, f, indent=2)

        print(f"[📸] Snapshot created: {snapshot_file}")
        return snapshot_file

    def list_snapshots(self) -> List[str]:
        if not os.path.exists(self.snapshot_dir):
            return []
        return [f for f in os.listdir(self.snapshot_dir) if f.endswith(".json")]

if __name__ == "__main__":
    snap = MemorySnapshot()
    snap.create_snapshot()
    print("[📁] Available snapshots:")
    for s in snap.list_snapshots():
        print(f"• {s}")
