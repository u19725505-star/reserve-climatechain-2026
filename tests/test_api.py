"""API-level regression tests for RESERVE's public demonstration contract.

These tests validate deterministic behavior with fictional demo data. They do
not validate operational performance or real-world climate outcomes.
"""
import unittest

from app import app


class TestEvaluationAPI(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    def evaluate(self, **overrides):
        payload = {
            "material": "recycled_plastic",
            "quantity_tonnes": 7,
            "required_quality": 0.8,
            "earliest_delivery_day": 5,
            "latest_delivery_day": 8,
        }
        payload.update(overrides)
        return self.client.post("/api/evaluate", json=payload)

    def test_health_endpoint_discloses_demo_status(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["release"], "0.3")
        self.assertEqual(body["data_status"], "fictional demo data")
        self.assertEqual(body["emissions_status"], "illustrative, not verified")

    def test_default_demo_has_two_eligible_processors(self):
        response = self.evaluate()
        self.assertEqual(response.status_code, 200)
        body = response.get_json()
        self.assertEqual(body["eligible_count"], 2)
        self.assertEqual(body["excluded_count"], 2)
        self.assertEqual(set(body["ranked_processor_names"]), {"Processor A", "Processor B"})
        self.assertEqual(body["selected"], "Processor B")

    def test_nearest_eligible_baseline_is_not_nearest_overall(self):
        body = self.evaluate().get_json()
        self.assertEqual(body["baseline"]["processor"], "Processor B")
        self.assertEqual(body["nearest_overall_processor"]["processor"], "Processor C")
        self.assertFalse(body["nearest_overall_processor"]["eligible"])
        self.assertIn(
            "Insufficient available processing capacity.",
            body["nearest_overall_processor"]["reasons"],
        )

    def test_uniform_illustrative_factor_does_not_claim_modeled_savings(self):
        body = self.evaluate().get_json()
        self.assertEqual(body["comparison"]["selected_processor"], "Processor B")
        self.assertEqual(body["comparison"]["estimated_avoided_kg_co2e"], 0.0)
        self.assertEqual(body["comparison"]["estimated_reduction_percent"], 0.0)
        self.assertIn("not measured or verified", body["comparison"]["interpretation"])
        self.assertIn("No verified emissions reduction", body["climate_impact_claim"])

    def test_no_eligible_processor_returns_null_baseline_and_comparison(self):
        body = self.evaluate(quantity_tonnes=30).get_json()
        self.assertEqual(body["eligible_count"], 0)
        self.assertIsNone(body["selected"])
        self.assertIsNone(body["baseline"]["processor"])
        self.assertIsNone(body["comparison"]["estimated_reduction_percent"])

    def test_invalid_inputs_are_rejected(self):
        cases = [
            ({"quantity_tonnes": 0}, "Quantity must be a finite number greater than zero."),
            ({"quantity_tonnes": -1}, "Quantity must be a finite number greater than zero."),
            ({"required_quality": 1.1}, "Quality must be a finite number between 0 and 1."),
            ({"material": "unknown"}, "Select a supported demonstration material."),
            ({"earliest_delivery_day": 9, "latest_delivery_day": 5}, "Delivery days must be non-negative and ordered."),
        ]
        for payload, expected_message in cases:
            with self.subTest(payload=payload):
                response = self.evaluate(**payload)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(response.get_json()["error"], expected_message)

    def test_non_json_request_body_is_rejected(self):
        response = self.client.post(
            "/api/evaluate",
            data="not json",
            content_type="text/plain",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.get_json()["error"],
            "Request body must be a JSON object.",
        )


if __name__ == "__main__":
    unittest.main()
