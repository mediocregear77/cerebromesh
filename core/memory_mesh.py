# File: core/memory_mesh.py

import json
import time
from typing import Dict, List, Optional
from uuid import uuid4

class MemoryEvent:
    def __init__(self, event_type: str, data: Dict[str, any], tags: Optional[List[str]] = None):
        self.event_id = str(uuid4())
        self.timestamp = int(time.time())
        self.event_type = event_type
        self.data = data
        self.tags = tags or []

    def to_dict(self) -> Dict:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "data": self.data,
            "tags": self.tags
        }

class MemoryMesh:
    def __init__(self):
        self.events: List[MemoryEvent] = []

    def log_event(self, event_type: str, data: Dict[str, any], tags: Optional[List[str]] = None):
        event = MemoryEvent(event_type, data, tags)
        self.events.append(event)
        return event.event_id

    def query_events(self, tag: Optional[str] = None, event_type: Optional[str] = None) -> List[Dict]:
        results = []
        for event in self.events:
            if tag and tag not in event.tags:
                continue
            if event_type and event.event_type != event_type:
                continue
            results.append(event.to_dict())
        return results

    def export_memory(self) -> List[Dict]:
        return [event.to_dict() for event in self.events]

    def save_to_file(self, filepath: str = "mesh_data/mesh_memory.json"):
        with open(filepath, "w") as f:
            json.dump(self.export_memory(), f, indent=2)

    def load_from_file(self, filepath: str = "mesh_data/mesh_memory.json"):
        try:
            with open(filepath, "r") as f:
                raw_events = json.load(f)
                self.events = [
                    MemoryEvent(
                        event["event_type"],
                        event["data"],
                        event.get("tags", [])
                    )
                    for event in raw_events
                ]
                for i, e in enumerate(raw_events):
                    self.events[i].event_id = e["event_id"]
                    self.events[i].timestamp = e["timestamp"]
        except FileNotFoundError:
            self.events = []
