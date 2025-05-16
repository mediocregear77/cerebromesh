# File: scripts/event_simulator.py

import time
import random
import json
from uuid import uuid4
from typing import List, Dict

EVENT_TYPES = ["route_created", "test_passed", "test_failed", "decision_logged", "scaling_forecast"]
ROUTES = ["/checkout", "/orders", "/cart", "/products"]
METHODS = ["GET", "POST", "PUT", "DELETE"]

def generate_event() -> Dict:
    event_type = random.choice(EVENT_TYPES)
    route = random.choice(ROUTES)
    method = random.choice(METHODS)
    timestamp = int(time.time())

    if event_type == "route_created":
        data = {"path": route, "method": method, "description": f"Auto-generated for {route}"}
        tags = ["api", "generation"]
    elif event_type == "test_passed":
        data = {"path": route, "status": "200 OK", "duration_ms": random.randint(50, 200)}
        tags = ["test", "success"]
    elif event_type == "test_failed":
        data = {"path": route, "status": "500 Error", "duration_ms": random.randint(100, 500)}
        tags = ["test", "failure"]
    elif event_type == "decision_logged":
        data = {
            "agent_id": f"agent-{random.randint(1,3)}",
            "action": {"type": "route_add", "path": route, "method": method, "confidence": round(random.uniform(0.4, 0.99), 2)},
            "allowed": random.choice([True, False])
        }
        tags = ["firewall", "decision"]
    elif event_type == "scaling_forecast":
        data = {
            "route": route,
            "expected_rps": round(random.uniform(100, 9000), 2),
            "recommendation": random.choice(["scale_up", "hold", "scale_down"])
        }
        tags = ["scaling", "forecast"]

    return {
        "event_id": str(uuid4()),
        "timestamp": timestamp,
        "event_type": event_type,
        "data": data,
        "tags": tags
    }

def simulate_events(n: int = 10) -> List[Dict]:
    return [generate_event() for _ in range(n)]

def save_events(events: List[Dict], filename: str = "mesh_data/simulated_events.json"):
    with open(filename, "w") as f:
        json.dump(events, f, indent=2)
    print(f"[💾] Saved {len(events)} simulated events to {filename}")

if __name__ == "__main__":
    simulated = simulate_events(20)
    save_events(simulated)
