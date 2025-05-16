# File: cli/cmesh_deploy.py

import argparse
import os
import shutil
import time
from pathlib import Path

def simulate_deploy(api_dir: str, provider: str, dry_run: bool = False):
    if not os.path.exists(api_dir):
        print(f"[!] API directory not found: {api_dir}")
        return

    build_dir = f"{api_dir}/build_{provider}_{int(time.time())}"
    if dry_run:
        print(f"[🔍] Dry run: would deploy contents of {api_dir} to {provider.upper()}")
        return

    os.makedirs(build_dir, exist_ok=True)
    for file in Path(api_dir).rglob("*"):
        if file.is_file():
            rel_path = file.relative_to(api_dir)
            dest_path = os.path.join(build_dir, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy(file, dest_path)

    print(f"[🚀] Deployed '{api_dir}' → provider: {provider.upper()} [output dir: {build_dir}]")

def main():
    parser = argparse.ArgumentParser(description="Deploy a generated CerebroMesh API to the cloud.")
    parser.add_argument("--dir", type=str, default="api_output/generated_api", help="Directory containing the API to deploy")
    parser.add_argument("--provider", type=str, choices=["cloudflare", "vercel", "docker", "local"], default="cloudflare", help="Deployment target")
    parser.add_argument("--dry", action="store_true", help="Simulate the deployment without executing")

    args = parser.parse_args()
    simulate_deploy(args.dir, args.provider, args.dry)

if __name__ == "__main__":
    main()
