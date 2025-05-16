# File: core/federated_learner.py

import hashlib
import json
from typing import Dict, List, Optional
from datetime import datetime
from uuid import uuid4

class FederatedLearner:
    def __init__(self):
        self.pattern_summaries: List[Dict[str, any]] = []
        self.org_opt_in: Dict[str, bool] = {}

    def opt_in(self, org_id: str):
        self.org_opt_in[org_id] = True

    def opt_out(self, org_id: str):
        self.org_opt_in[org_id] = False

    def is_enrolled(self, org_id: str) -> bool:
        return self.org_opt_in.get(org_id, False)

    def submit_pattern(self, org_id: str, pattern: Dict[str, any]) -> Optional[str]:
        if not self.is_enrolled(org_id):
            return None

        fingerprint = self._anonymize_pattern(pattern)
        summary = {
            "pattern_id": str(uuid4()),
            "org_id_hash": hashlib.sha256(org_id.encode()).hexdigest(),
            "timestamp": datetime.utcnow().isoformat(),
            "pattern_fingerprint": fingerprint,
        }
        self.pattern_summaries.append(summary)
        return summary["pattern_id"]

    def get_common_patterns(self, limit: int = 10) -> List[Dict[str, any]]:
        # Return the most recent pattern fingerprints
        return sorted(
            self.pattern_summaries,
            key=lambda x: x["timestamp"],
            reverse=True
        )[:limit]

    def _anonymize_pattern(self, pattern: Dict[str, any]) -> str:
        """Hashes structure and keys to preserve semantic similarity without exposing content."""
        raw = json.dumps(sorted(pattern.keys()))
        return hashlib.sha256(raw.encode()).hexdigest()
