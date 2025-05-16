# File: marketplace/composer.py

import json
from typing import List, Dict, Any
from uuid import uuid4
from datetime import datetime
import os

class APIComposer:
    def __init__(self):
        self.compositions: List[Dict[str, Any]] = []

    def compose(self, apis: List[Dict[str, Any]]) -> Dict[str, Any]:
        combined_endpoints = []
        combined_metadata = {
            "composition_id": str(uuid4()),
            "created_at": datetime.utcnow().isoformat(),
            "sources": []
        }

        for api in apis:
            combined_metadata["sources"].append({
                "listing_id": api.get("listing_id"),
                "name": api.get("name"),
                "version": api.get("version")
            })
            combined_endpoints.extend(api.get("endpoints", []))

        composition = {
            "metadata": combined_metadata,
            "endpoints": list(set(combined_endpoints))  # Remove duplicates
        }

        self.compositions.append(composition)
        return composition

    def save_composition(self, composition: Dict[str, Any], directory: str = "marketplace/compositions"):
        os.makedirs(directory, exist_ok=True)
        file_path = os.path.join(directory, f"{composition['metadata']['composition_id']}.json")
        with open(file_path, "w") as f:
            json.dump(composition, f, indent=2)
        return file_path

    def list_compositions(self) -> List[Dict[str, Any]]:
        return self.compositions
