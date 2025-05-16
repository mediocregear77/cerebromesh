# File: scripts/log_scrubber.py

import json
import os
from typing import List, Dict
from datetime import datetime

class LogScrubber:
    def __init__(self, input_path: str = "mesh_data/mesh_memory.json", output_path: str = "mesh_data/scrubbed_memory.json"):
        self.input_path = input_path
        self.output_path = output_path
        self.scrubbed_logs: List[Dict] = []

    def load_logs(self) -> List[Dict]:
        if not os.path.exists(self.input_path):
            print(f"[!] Log file not found: {self.input_path}")
            return []
        with open(self.input_path, "r") as f:
            return json.load(f)

    def scrub(self, redact_fields: List[str] = ["user_id", "email", "token"]):
        logs = self.load_logs()
        for event in logs:
            data = event.get("data", {})
            for field in redact_fields:
                if field in data:
                    data[field] = "[REDACTED]"
            event["data"] = data
            event["scrubbed_at"] = datetime.utcnow().isoformat()
            self.scrubbed_logs.append(event)

    def save_scrubbed_logs(self):
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)
        with open(self.output_path, "w") as f:
            json.dump(self.scrubbed_logs, f, indent=2)
        print(f"[🧼] Scrubbed logs saved to {self.output_path}")

    def run(self, redact_fields: List[str] = None):
        self.scrub(redact_fields or ["user_id", "email", "token"])
        self.save_scrubbed_logs()

if __name__ == "__main__":
    scrubber = LogScrubber()
    scrubber.run()
