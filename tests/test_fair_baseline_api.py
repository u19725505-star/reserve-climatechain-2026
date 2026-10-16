"""API checks for fair baseline comparison and explicit no-candidate handling."""

import unittest

from app import app
from reserve.demo_data import demo_processors


class TestFairBaselineAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_default_scenario_uses_nearest_eligible_baseline(self):
        response = self.client.post("/api/evaluate", json={
            "material": "recycled_plastic",
            "quantity_tonnes": 10,
            "required_quality": 0.8,
            "earliest_delivery_day": 5,
            "latest_delivery_day": 8,
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["baseline"]["processor"], "Processor B")
        self.assertTrue(data["baseline"]["eligible"])
        self.assertEqual(data["comparison"]["selected_processor"], "Processor B")
        self.assertEqual(data["comparison"]["estimated_avoided_kg_co2e"], 0.0)
        self.assertEqual(data["comparison"]["estimated_reduction_percent"], 0.0)

    def test_web_api_uses_shared_demo_processor_profiles(self):
        response = self.client.post("/api/evaluate", json={
            "material": "recycled_plastic",
            "quantity_tonnes": 10,
            "required_quality": 0.8,
            "earliest_delivery_day": 5,
            "latest_delivery_day": 8,
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        expected = {p.name: p for p in demo_processors()}
        actual = {p["name"]: p for p in data["processors"]}
        self.assertEqual(set(actual), set(expected))
        for name, processor in expected.items():
            self.assertEqual(actual[name]["distance_km"], processor.distance_km)
            self.assertEqual(actual[name]["capacity_tonnes"], processor.available_capacity_tonnes)
            self.assertEqual(actual[name]["accepted_materials"], list(processor.accepted_materials))

    def test_non_object_json_is_rejected_cleanly(self):
        for payload in ([], "text", 7):
            response = self.client.post("/api/evaluate", json=payload)
            self.assertEqual(response.status_code, 400)

    def test_non_finite_quantity_is_rejected(self):
        for quantity in (float("inf"), float("-inf"), float("nan")):
            response = self.client.post("/api/evaluate", json={
                "material": "recycled_plastic",
                "quantity_tonnes": quantity,
                "required_quality": 0.8,
                "earliest_delivery_day": 5,
                "latest_delivery_day": 8,
            })
            self.assertEqual(response.status_code, 400)

    def test_no_eligible_candidate_has_no_fabricated_baseline(self):
        response = self.client.post("/api/evaluate", json={
            "material": "glass",
            "quantity_tonnes": 10,
            "required_quality": 0.8,
            "earliest_delivery_day": 5,
            "latest_delivery_day": 8,
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsNone(data["baseline"]["processor"])
        self.assertIsNone(data["comparison"]["estimated_reduction_percent"])
        self.assertIsNone(data["selected"])


if __name__ == "__main__":
    unittest.main()
