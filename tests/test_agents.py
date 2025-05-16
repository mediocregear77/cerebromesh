# File: tests/test_agents.py

import unittest
from core.swarm_agents import RLAgent

class TestRLAgent(unittest.TestCase):
    def setUp(self):
        self.agent = RLAgent()
        self.state = "test_state"
        self.next_state = "next_state"
        self.action = "test:POST:/checkout"
        self.actions = [self.action, "test:GET:/cart"]

    def test_choose_action_exploration_or_exploitation(self):
        # Force exploitation for test predictability
        self.agent.exploration_rate = 0.0
        self.agent.q_table[f"{self.state}:{self.action}"] = 0.9
        chosen = self.agent.choose_action(self.state, self.actions)
        self.assertEqual(chosen, self.action)

    def test_update_q_value_increases_value(self):
        self.agent.update_q_value(self.state, self.action, 1.0, self.next_state, self.actions)
        updated_value = self.agent.q_table.get(f"{self.state}:{self.action}")
        self.assertIsNotNone(updated_value)
        self.assertGreater(updated_value, 0.0)

    def test_run_test_case_returns_result(self):
        route = {"path": "/checkout", "method": "POST"}
        payload = {"user_id": 123}
        result = self.agent.run_test_case(route, payload)
        self.assertIn("agent_id", result)
        self.assertIn("outcome", result)
        self.assertIn("reward", result)

    def test_export_q_table_not_empty(self):
        self.agent.update_q_value(self.state, self.action, 1.0, self.next_state, self.actions)
        q_table = self.agent.export_q_table()
        self.assertTrue(len(q_table) > 0)

if __name__ == '__main__':
    unittest.main()
