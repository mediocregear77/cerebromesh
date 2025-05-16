# File: compliance/privacy_tags.py

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import hashlib
import json

class PrivacyTagger:
    def __init__(self):
        self.tagged_fields: Dict[str, Dict[str, any]] = {}

    def tag_field(self, route: str, field: str, tags: List[str], ttl_days: Optional[int] = None):
        """Assigns privacy tags (e.g., 'PII', 'GDPR', 'HIPAA') and optional TTL to a field."""
        key = f"{route}:{field}"
        expiration = None
        if ttl_days is not None:
            expiration = (datetime.utcnow() + timedelta(days=ttl_days)).isoformat()

        self.tagged_fields[key] = {
            "tags": tags,
            "ttl": expiration
        }

    def get_tag(self, route: str, field: str) -> Dict[str, any]:
        key = f"{route}:{field}"
        return self.tagged_fields.get(key, {})

    def export_tags(self) -> Dict[str, Dict[str, any]]:
        return self.tagged_fields

    def save_to_file(self, path: str = "mesh_data/privacy_tags.json"):
        with open(path, "w") as f:
            json.dump(self.export_tags(), f, indent=2)

    def load_from_file(self, path: str = "mesh_data/privacy_tags.json"):
        try:
            with open(path, "r") as f:
                self.tagged_fields = json.load(f)
        except FileNotFoundError:
            self.tagged_fields = {}

    def check_expired_fields(self) -> List[str]:
        expired = []
        now = datetime.utcnow()
        for key, meta in self.tagged_fields.items():
            ttl = meta.get("ttl")
            if ttl and datetime.fromisoformat(ttl) < now:
                expired.append(key)
        return expired
