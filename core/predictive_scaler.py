# File: core/predictive_scaler.py

import time
import random
from typing import Dict, List, Optional
from statistics import mean, stdev
from uuid import uuid4

class ScalingForecast:
    def __init__(self):
        self.history: List[Dict[str, any]] = []
        self.forecasts: List[Dict[str, any]] = []

    def log_traffic_sample(self, route: str, rps: float):
        self.history.append({
            "timestamp": int(time.time()),
            "route": route,
            "rps": rps
        })

    def forecast_load(self, route: str, window: int = 10) -> Dict[str, float]:
        recent = [h["rps"] for h in self.history if h["route"] == route][-window:]
        if not recent:
            return {"expected_rps": 0.0, "stdev": 0.0, "recommendation": "hold"}

        avg = mean(recent)
        deviation = stdev(recent) if len(recent) > 1 else 0.0
        forecast = {
            "expected_rps": avg,
            "stdev": deviation,
            "recommendation": self._recommend(avg, deviation)
        }

        self.forecasts.append({
            "timestamp": int(time.time()),
            "route": route,
            "forecast": forecast
        })

        return forecast

    def _recommend(self, avg: float, deviation: float) -> str:
        if avg > 5000 or (avg > 1000 and deviation > 300):
            return "scale_up"
        elif avg < 100 and deviation < 50:
            return "scale_down"
        return "hold"

    def export_forecasts(self) -> List[Dict]:
        return self.forecasts

    def simulate_sample_data(self, route: str, count: int = 20):
        for _ in range(count):
            self.log_traffic_sample(route, random.uniform(100, 8000))
