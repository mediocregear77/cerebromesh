# File: cli/cmesh_explain.py

import json
import argparse
import os
from typing import Dict, Any

def load_routes(filepath: str) -> Dict[str, Any]:
    if not os.path.exists(filepath):
        print(f"[!] Route file not found: {filepath}")
        return {}
    with open(filepath, "r") as f:
        return json.load(f)

def explain_route(route_data: Dict[str, Any], route_id: str):
    route = route_data.get(route_id)
    if not route:
        print(f"[!] Route ID '{route_id}' not found.")
        return

    print(f"\n[🔍] Explaining Route ID: {route_id}")
    print(f"→ Path: {route['path']}")
    print(f"→ Method: {route['method']}")
    print(f"→ Schema:")
    for field, meta in route['schema']['properties'].items():
        print(f"   - {field} ({meta.get('type', 'unknown')})")

    print("\n[🧠] Reasoning:")
    print("This route was generated based on schema structure and typical REST design patterns.")
    if 'checkout' in route['path']:
        print("• Recognized 'checkout' as transactional flow.")
    elif 'cart' in route['path']:
        print("• Recognized 'cart' as session-based user interaction.")
    else:
        print("• No specific heuristics matched—default schema applied.")

def main():
    parser = argparse.ArgumentParser(description="Explain a CerebroMesh route by its ID.")
    parser.add_argument("route_id", type=str, help="ID of the route to explain")
    parser.add_argument("--file", type=str, default="api_output/generated_api/generated_routes.json", help="Path to the routes JSON file")

    args = parser.parse_args()

    routes = load_routes(args.file)
    explain_route(routes, args.route_id)

if __name__ == "__main__":
    main()
