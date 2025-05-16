# File: compliance/owasp_validator.py

import json
from typing import List, Dict
from datetime import datetime
from uuid import uuid4

class OWASPValidator:
    def __init__(self):
        self.issues: List[Dict[str, any]] = []

    def validate(self, api_routes: List[Dict[str, any]]) -> List[Dict[str, any]]:
        self.issues = []
        for route in api_routes:
            path = route.get("path", "")
            method = route.get("method", "GET")

            if not path.startswith("/"):
                self._log_issue(path, method, "Invalid route format", "A01 - Broken Access Control")

            if "id" in path and "GET" not in method:
                self._log_issue(path, method, "Unprotected parameterized route", "A05 - Security Misconfiguration")

            if method == "POST" and not self._has_auth_guard(route):
                self._log_issue(path, method, "Missing authentication check", "A07 - Identification and Authentication Failures")

        return self.issues

    def _has_auth_guard(self, route: Dict[str, any]) -> bool:
        # Placeholder for detection logic
        # In real systems, this would inspect decorators or middleware flags
        return "auth_required" in route.get("tags", [])

    def _log_issue(self, path: str, method: str, description: str, owasp_category: str):
        self.issues.append({
            "issue_id": str(uuid4()),
            "timestamp": datetime.utcnow().isoformat(),
            "path": path,
            "method": method,
            "description": description,
            "owasp_category": owasp_category
        })

    def export_issues(self) -> List[Dict[str, any]]:
        return self.issues
