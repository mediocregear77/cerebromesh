# File: cli/cmesh_audit.py

import json
import argparse
import os
from datetime import datetime

def load_audits(filepath: str) -> list:
    if not os.path.exists(filepath):
        print(f"[!] Audit file not found: {filepath}")
        return []
    with open(filepath, "r") as f:
        return json.load(f)

def summarize_audits(audits: list, risk_threshold: int = 50):
    print(f"\n[🛡️] Compliance Audit Summary")
    print("=" * 40)

    for audit in audits:
        status = "✅ PASS" if audit["status"] == "pass" else "❌ FAIL"
        risk = audit.get("risk_score", 0)
        alert = "⚠️ HIGH RISK" if risk >= risk_threshold else ""
        ts = datetime.fromtimestamp(audit["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        print(f"{status} — {audit['module']} @ {ts}")
        print(f"• Risk Score: {risk} {alert}")
        print(f"• Notes: {audit['notes']}")
        print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Audit CerebroMesh module compliance status.")
    parser.add_argument("--file", type=str, default="mesh_data/compliance_audits.json", help="Path to the compliance audit file")
    parser.add_argument("--risk", type=int, default=50, help="Risk score threshold to flag high risk modules")

    args = parser.parse_args()
    audits = load_audits(args.file)
    summarize_audits(audits, args.risk)

if __name__ == "__main__":
    main()
