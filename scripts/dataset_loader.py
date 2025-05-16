# File: scripts/dataset_loader.py

import os
import json
from typing import Dict, List

class DatasetLoader:
    def __init__(self, base_path: str = "datasets"):
        self.base_path = base_path
        self.loaded_data: Dict[str, List[Dict]] = {}

    def load_all(self) -> Dict[str, List[Dict]]:
        if not os.path.exists(self.base_path):
            print(f"[!] Dataset path not found: {self.base_path}")
            return {}

        for root, _, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".json"):
                    path = os.path.join(root, file)
                    topic = os.path.splitext(file)[0]
                    with open(path, "r") as f:
                        try:
                            data = json.load(f)
                            if isinstance(data, list):
                                self.loaded_data[topic] = data
                            elif isinstance(data, dict):
                                self.loaded_data[topic] = [data]
                        except Exception as e:
                            print(f"[!] Failed to load {file}: {e}")
        return self.loaded_data

    def get_topic(self, topic: str) -> List[Dict]:
        return self.loaded_data.get(topic, [])

    def summary(self) -> Dict[str, int]:
        return {topic: len(entries) for topic, entries in self.loaded_data.items()}

if __name__ == "__main__":
    loader = DatasetLoader()
    datasets = loader.load_all()
    print("[📦] Loaded Topics:")
    for topic, count in loader.summary().items():
        print(f"• {topic}: {count} entries")
