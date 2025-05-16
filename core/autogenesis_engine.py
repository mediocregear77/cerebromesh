# File: core/autogenesis_engine.py

import json
from typing import Dict, List, Optional, Any
from fastapi import APIRouter
from pydantic import BaseModel, create_model
from uuid import uuid4

class APIGenerator:
    def __init__(self):
        self.routes: Dict[str, Any] = {}
        self.schemas: Dict[str, BaseModel] = {}

    def generate_schema(self, name: str, fields: Dict[str, str]) -> BaseModel:
        """Dynamically creates a Pydantic model based on fields."""
        annotations = {k: eval(v) for k, v in fields.items()}
        model = create_model(name, **annotations)
        self.schemas[name] = model
        return model

    def generate_route(self, path: str, method: str, model: BaseModel) -> Dict[str, Any]:
        """Generates route metadata and stores it."""
        route_id = str(uuid4())
        self.routes[route_id] = {
            "path": path,
            "method": method.upper(),
            "model": model,
        }
        return self.routes[route_id]

    def export_routes(self) -> Dict[str, Any]:
        """Returns all generated routes for inspection or serialization."""
        return {
            route_id: {
                "path": data["path"],
                "method": data["method"],
                "schema": data["model"].schema()
            }
            for route_id, data in self.routes.items()
        }

    def build_router(self) -> APIRouter:
        """Builds a FastAPI router from generated routes."""
        router = APIRouter()
        for route_id, data in self.routes.items():
            path = data["path"]
            model = data["model"]
            method = data["method"]

            async def endpoint(payload: model):  # type: ignore
                return {"message": f"{method} to {path} accepted", "payload": payload.dict()}

            router.add_api_route(
                path,
                endpoint,
                methods=[method],
                response_model=model
            )
        return router
