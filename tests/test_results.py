
"""Tests for RESERVE structured JSON results."""

import json
import tempfile
import unittest
from pathlib import Path

from reserve.results import build_results_record, save_results_json


class TestResults(unittest.TestCase):
    def setUp(self):
        self.shipment = {
            "material": "recycled_plastic",
            "quantity_tonnes": 10.0,
            "required_quality": 0.8,
            "earliest_delivery_day": 5,
            "latest_delivery_day": 8,
        }

        self.candidates = [
            {
                "processor": "Processor B",
                "eligible": True,
                "distance_km": 15.0,
                "estimated_emissions_kg_co2e": 15.0,
                "reasons": [],
            },
            {
                "processor": "Processor A",
                "eligible": True,
                "distance_km": 25.0,
                "estimated_emissions_kg_co2e": 25.0,
                "reasons": [],
            },
        ]

    def test_record_contains_required_fields(self):
        record = build_results_record(
            shipment=self.shipment,
            ranked_candidates=self.candidates,
            emission_factor_kg_per_tonne_km=0.1,
        )

        self.assertEqual(record["project"], "RESERVE")
        self.assertEqual(record["schema_version"], "1.0")
        self.assertEqual(record["shipment"]["material"], "recycled_plastic")
        self.assertEqual(len(record["ranked_processors"]), 2)

    def test_processor_ranking_is_preserved(self):
        record = build_results_record(
            shipment=self.shipment,
            ranked_candidates=self.candidates,
            emission_factor_kg_per_tonne_km=0.1,
        )

        ranked = record["ranked_processors"]
        self.assertEqual(ranked[0]["processor"], "Processor B")
        self.assertEqual(ranked[0]["rank"], 1)
        self.assertEqual(ranked[1]["processor"], "Processor A")
        self.assertEqual(ranked[1]["rank"], 2)

    def test_record_states_emissions_limitations(self):
        record = build_results_record(
            shipment=self.shipment,
            ranked_candidates=self.candidates,
            emission_factor_kg_per_tonne_km=0.1,
        )

        self.assertIn("not verified", record["emissions"]["status"])
        self.assertIn("No verified emissions reduction",
                      record["climate_impact_claim"])
        self.assertEqual(
            record["data_status"],
            "synthetic demonstration data",
        )

    def test_negative_emission_factor_is_rejected(self):
        with self.assertRaises(ValueError):
            build_results_record(
                shipment=self.shipment,
                ranked_candidates=self.candidates,
                emission_factor_kg_per_tonne_km=-0.1,
            )

    def test_saved_json_can_be_loaded(self):
        record = build_results_record(
            shipment=self.shipment,
            ranked_candidates=self.candidates,
            emission_factor_kg_per_tonne_km=0.1,
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "results.json"
            saved_path = save_results_json(record, output_path)

            self.assertTrue(saved_path.exists())

            with saved_path.open("r", encoding="utf-8") as file:
                loaded = json.load(file)

            self.assertEqual(loaded["project"], "RESERVE")
            self.assertEqual(
                loaded["ranked_processors"][0]["processor"],
                "Processor B",
            )


if __name__ == "__main__":
    unittest.main()