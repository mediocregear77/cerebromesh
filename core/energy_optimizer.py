# File: core/energy_optimizer.py

import random
from typing import Dict, List, Optional
from datetime import datetime

class EnergyProfile:
    def __init__(self):
        # Sample region carbon intensity scores (gCO2eq/kWh)
        self.region_profiles = {
            "us-west": 120,
            "us-east": 230,
            "eu-central": 80,
            "ap-southeast": 150
        }

        # Sample deployment cost per 1M requests
        self.region_costs = {
            "us-west": 2.50,
            "us-east": 2.80,
            "eu-central": 2.70,
            "ap-southeast": 3.10
        }

    def get_best_region(self, priority: str = "eco") -> Dict[str, any]:
        if priority == "eco":
            best_region = min(self.region_profiles, key=self.region_profiles.get)
        elif priority == "cost":
            best_region = min(self.region_costs, key=self.region_costs.get)
        else:
            # Default hybrid scoring
            hybrid_score = {
                region: self.region_profiles[region] * 0.5 + self.region_costs[region] * 0.5
                for region in self.region_profiles
            }
            best_region = min(hybrid_score, key=hybrid_score.get)

        return {
            "region": best_region,
            "carbon_score": self.region_profiles[best_region],
            "estimated_cost": self.region_costs[best_region],
            "timestamp": datetime.utcnow().isoformat()
        }

    def compare_regions(self) -> List[Dict[str, any]]:
        return [
            {
                "region": region,
                "carbon_score": self.region_profiles[region],
                "estimated_cost": self.region_costs[region],
            }
            for region in self.region_profiles
        ]

    def log_decision(self, chosen_region: str, reason: str) -> Dict[str, str]:
        return {
            "region": chosen_region,
            "reason": reason,
            "timestamp": datetime.utcnow().isoformat()
        }
