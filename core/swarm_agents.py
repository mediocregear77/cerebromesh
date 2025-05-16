# File: core/swarm_agents.py

import random
import json
from typing import Any, Dict, List
from uuid import uuid4

class RLAgent:
    def __init__(self, agent_id: Optional[str] = None):
        self.agent_id = agent_id or str(uuid4())
        self.q_table: Dict[str, float] = {}
        self.exploration_rate = 0.2
        self.learning_rate = 0.1
        self.discount_factor = 0.9

    def choose_action(self, state: str, possible_actions: List[str]) -> str:
        if random.random() < self.exploration_rate:
            return random.choice(possible_actions)
        else:
            q_values = {a: self.q_table.get(f"{state}:{a}", 0.0) for a in possible_actions}
            return max(q_values, key=q_values.get)

    def update_q_value(self, state: str, action: str, reward: float, next_state: str, next_actions: List[str]):
        max_next_q = max([self.q_table.get(f"{next_state}:{a}", 0.0) for a in next_actions], default=0.0)
        old_q = self.q_table.get(f"{state}:{action}", 0.0)
        new_q = old_q + self.learning_rate * (reward + self.discount_factor * max_next_q - old_q)
        self.q_table[f"{state}:{action}"] = new_q

    def run_test_case(self, route: Dict[str, Any], payload: Dict[str, Any]) -> Dict[str, Any]:
        """Simulates a test case run on a given route and returns the result."""
        # Dummy simulation of an API call
        outcome = random.choice(["pass", "fail", "timeout", "invalid"])
        reward = {"pass": 1.0, "fail": -1.0, "timeout": -0.5, "invalid": -0.8}[outcome]
        action = f"test:{route['method']}:{route['path']}"
        self.update_q_value("test_state", action, reward, "next_state", [action])
        return {
            "agent_id": self.agent_id,
            "route": route,
            "outcome": outcome,
            "reward": reward
        }

    def export_q_table(self) -> Dict[str, float]:
        return self.q_table
