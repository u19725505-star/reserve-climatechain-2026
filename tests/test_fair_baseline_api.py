"""API checks for fair baseline comparison and explicit no-candidate handling."""

import unittest

from app import app


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
