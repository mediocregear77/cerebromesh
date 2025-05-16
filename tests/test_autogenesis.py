# File: tests/test_autogenesis.py

import unittest
from core.autogenesis_engine import APIGenerator

class TestAutogenesisEngine(unittest.TestCase):
    def setUp(self):
        self.generator = APIGenerator()
        self.fields = {
            "user_id": "int",
            "email": "str",
            "is_active": "bool"
        }

    def test_generate_schema(self):
        model = self.generator.generate_schema("UserModel", self.fields)
        instance = model(user_id=1, email="test@example.com", is_active=True)
        self.assertEqual(instance.user_id, 1)
        self.assertEqual(instance.email, "test@example.com")
        self.assertTrue(instance.is_active)

    def test_generate_route_and_export(self):
        model = self.generator.generate_schema("SessionModel", {
            "session_id": "str",
            "timestamp": "float"
        })
        route = self.generator.generate_route("/sessions", "POST", model)
        exported = self.generator.export_routes()
        self.assertIn(route["path"], [r["path"] for r in exported.values()])
        self.assertEqual(route["method"], "POST")

    def test_schema_fields(self):
        model = self.generator.generate_schema("LoginModel", {
            "username": "str",
            "password": "str"
        })
        schema = model.schema()
        self.assertIn("username", schema["properties"])
        self.assertIn("password", schema["properties"])

if __name__ == '__main__':
    unittest.main()
