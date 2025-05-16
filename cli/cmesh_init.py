# File: cli/cmesh_init.py

import argparse
import json
import os
from core.autogenesis_engine import APIGenerator

def load_schema(filepath: str) -> dict:
    with open(filepath, "r") as f:
        return json.load(f)

def save_output(api_data: dict, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, "generated_routes.json"), "w") as f:
        json.dump(api_data, f, indent=2)

def main():
    parser = argparse.ArgumentParser(description="Initialize a CerebroMesh API from a schema or prompt.")
    parser.add_argument("input", type=str, help="Path to schema.json or prompt.txt")
    parser.add_argument("--type", type=str, choices=["schema", "prompt"], default="schema")
    parser.add_argument("--output", type=str, default="api_output/generated_api", help="Output directory")

    args = parser.parse_args()

    generator = APIGenerator()

    if args.type == "schema":
        schema = load_schema(args.input)
        for route_def in schema.get("routes", []):
            model = generator.generate_schema(route_def["model"], route_def["fields"])
            generator.generate_route(route_def["path"], route_def["method"], model)
    else:
        print("Prompt-based generation is not implemented yet. Use type=schema for now.")
        return

    routes = generator.export_routes()
    save_output(routes, args.output)
    print(f"[✔] API initialized with {len(routes)} route(s). Output saved to: {args.output}")

if __name__ == "__main__":
    main()
