# File: tests/test_memory.py

import unittest
import os
import json
from core.memory_mesh import MemoryMesh

class TestMemoryMesh(unittest.TestCase):
    def setUp(self):
        self.mesh = MemoryMesh()
        self.event_type = "route_created"
        self.data = {"path": "/test", "method": "POST"}
        self.tags = ["test", "api"]

    def test_log_event_creates_entry(self):
        event_id = self.mesh.log_event(self.event_type, self.data, self.tags)
        self.assertTrue(len(self.mesh.events) == 1)
        self.assertEqual(self.mesh.events[0].event_id, event_id)

    def test_query_events_by_tag(self):
        self.mesh.log_event(self.event_type, self.data, self.tags)
        results = self.mesh.query_events(tag="api")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["data"]["path"], "/test")

    def test_query_events_by_type(self):
        self.mesh.log_event("test_passed", {"status": "200"}, ["test"])
        results = self.mesh.query_events(event_type="test_passed")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["event_type"], "test_passed")

    def test_save_and_load_memory_file(self):
        filepath = "tests/temp_memory.json"
        self.mesh.log_event("checkpoint", {"version": "1.0"}, ["tagged"])
        self.mesh.save_to_file(filepath)

        mesh2 = MemoryMesh()
        mesh2.load_from_file(filepath)
        self.assertEqual(len(mesh2.events), 1)
        self.assertEqual(mesh2.events[0].event_type, "checkpoint")
        os.remove(filepath)

if __name__ == "__main__":
    unittest.main()
