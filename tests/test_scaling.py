# File: tests/test_scaling.py

import unittest
from core.predictive_scaler import ScalingForecast

class TestScalingForecast(unittest.TestCase):
    def setUp(self):
        self.forecaster = ScalingForecast()
        self.route = "/checkout"

    def test_log_traffic_sample_adds_entry(self):
        self.forecaster.log_traffic_sample(self.route, 1200.5)
        self.assertEqual(len(self.forecaster.history), 1)
        self.assertEqual(self.forecaster.history[0]["route"], self.route)

    def test_forecast_load_returns_dict(self):
        for rps in [1000, 1200, 1100, 1300, 1050]:
            self.forecaster.log_traffic_sample(self.route, rps)
        forecast = self.forecaster.forecast_load(self.route)
        self.assertIn("expected_rps", forecast)
        self.assertIn("recommendation", forecast)

    def test_recommend_scale_up(self):
        for _ in range(10):
            self.forecaster.log_traffic_sample(self.route, 6000)
        forecast = self.forecaster.forecast_load(self.route)
        self.assertEqual(forecast["recommendation"], "scale_up")

    def test_recommend_scale_down(self):
        for _ in range(10):
            self.forecaster.log_traffic_sample(self.route, 50)
        forecast = self.forecaster.forecast_load(self.route)
        self.assertEqual(forecast["recommendation"], "scale_down")

    def test_recommend_hold(self):
        for _ in range(10):
            self.forecaster.log_traffic_sample(self.route, 500)
        forecast = self.forecaster.forecast_load(self.route)
        self.assertEqual(forecast["recommendation"], "hold")

if __name__ == "__main__":
    unittest.main()
