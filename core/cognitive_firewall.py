# File: core/cognitive_firewall.py

from typing import Dict, Any, List
from uuid import uuid4
import time

class CognitiveFirewall:
    def __init__(self):
        self.rules: List[Dict[str, Any]] = []
        self.decision_log: List[Dict[str, Any]] = []

    def add_rule(self, rule: Dict[str, Any]):
        """Adds a new validation rule to the firewall."""
        self.rules.append(rule)

    def evaluate_action(self, agent_id: str, action: Dict[str, Any]) -> bool:
        """
        Evaluates whether an agent's action is safe to execute based on current rules.
        Each rule is a dictionary with optional keys: 'action_type', 'path', 'method', 'confidence_threshold'.
        """
        allowed = True
        for rule in self.rules:
            if 'action_type' in rule and rule['action_type'] != action.get('type'):
                continue
            if 'path' in rule and rule['path'] != action.get('path'):
                continue
            if 'method' in rule and rule['method'] != action.get('method'):
                continue
            if 'confidence_threshold' in rule:
                if action.get('confidence', 1.0) < rule['confidence_threshold']:
                    allowed = False
                    break

        self.log_decision(agent_id, action, allowed)
        return allowed

    def log_decision(self, agent_id: str, action: Dict[str, Any], allowed: bool):
        log_entry = {
            "log_id": str(uuid4()),
            "timestamp": int(time.time()),
            "agent_id": agent_id,
            "action": action,
            "allowed": allowed
        }
        self.decision_log.append(log_entry)

    def get_logs(self) -> List[Dict[str, Any]]:
        return self.decision_log

    def clear_logs(self):
        self.decision_log = []
