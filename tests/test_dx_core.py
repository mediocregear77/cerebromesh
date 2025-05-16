# File: tests/test_dx_core.py

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from pydantic import BaseModel
from core.autogenesis_engine import APIGenerator

app = FastAPI()
generator = APIGenerator()

# Create a dummy model and route to attach to the app for testing
class ExampleModel(BaseModel):
    name: str
    age: int

generator.generate_route("/test", "POST", ExampleModel)
router = generator.build_router()
app.include_router(router)

client = TestClient(app)

class TestDXCore(unittest.TestCase):
    def test_route_exists_and_accepts_post(self):
        response = client.post("/test", json={"name": "Alice", "age": 30})
        self.assertEqual(response.status_code, 200)
        self.assertIn("message", response.json())
        self.assertIn("payload", response.json())
        self.assertEqual(response.json()["payload"]["name"], "Alice")

    def test_route_rejects_invalid_payload(self):
        response = client.post("/test", json={"name": "Bob"})
        self.assertEqual(response.status_code, 422)

    def test_route_schema_integrity(self):
        routes = generator.export_routes()
        self.assertTrue("/test" in [r["path"] for r in routes.values()])
        model_schema = list(routes.values())[0]["schema"]
        self.assertIn("name", model_schema["properties"])
        self.assertIn("age", model_schema["properties"])

if __name__ == "__main__":
    unittest.main()
