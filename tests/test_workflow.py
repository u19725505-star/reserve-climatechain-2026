"""
RESERVE — End-to-End Workflow Tests

Checks that eligibility filtering, processor ranking, and
report formatting work together as one workflow.
"""

import unittest

# Import the data structures used to define a shipment and candidates.
from src.reserve.evaluation import Processor, Shipment

# Import the ranking and report components.
from src.reserve.ranking import rank_eligible_processors
from src.reserve.report import format_processor_report


class TestReserveWorkflow(unittest.TestCase):
    """Verify that the main RESERVE components work together."""

    def setUp(self):
        # Define one fictional shipment for the integration tests.
        self.shipment = Shipment(
            material="recycled_plastic",
            quantity_tonnes=10,
            required_quality=0.8,
            earliest_delivery_day=5,
            latest_delivery_day=8,
        )

        # Define a farther candidate that meets the requirements.
        self.far_candidate = Processor(
            name="Far Processor",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=25,
        )

        # Define a nearer candidate that also meets the requirements.
        self.near_candidate = Processor(
            name="Near Processor",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=10,
        )

        # Define a candidate that fails the capacity requirement.
        self.ineligible_candidate = Processor(
            name="Ineligible Processor",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=5,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=1,
        )

    def test_workflow_ranks_eligible_candidates(self):
        """Eligible candidates should appear in emissions order."""
        ranked = rank_eligible_processors(
            shipment=self.shipment,
            processors=[
                self.far_candidate,
                self.ineligible_candidate,
                self.near_candidate,
            ],
            emission_factor_kg_per_tonne_km=0.1,
        )

        # The nearer candidate should rank first with this factor.
        self.assertEqual(
            [item["processor"] for item in ranked],
            ["Near Processor", "Far Processor"],
        )

        # The ineligible candidate must not appear in the results.
        self.assertNotIn(
            "Ineligible Processor",
            [item["processor"] for item in ranked],
        )

    def test_report_displays_workflow_results(self):
        """The report should display the ranking and estimates."""
        ranked = rank_eligible_processors(
            shipment=self.shipment,
            processors=[self.far_candidate, self.near_candidate],
            emission_factor_kg_per_tonne_km=0.1,
        )

        report = format_processor_report(ranked)

        self.assertIn("Near Processor", report)
        self.assertIn("Far Processor", report)
        self.assertIn("screening estimates", report)

    def test_no_eligible_candidates_produces_clear_report(self):
        """An empty ranking should be reported clearly."""
        ranked = rank_eligible_processors(
            shipment=self.shipment,
            processors=[self.ineligible_candidate],
            emission_factor_kg_per_tonne_km=0.1,
        )

        report = format_processor_report(ranked)

        self.assertIn("No eligible processors were found", report)


# Allow the integration tests to be run directly.
if __name__ == "__main__":
    unittest.main()
