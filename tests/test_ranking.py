"""
RESERVE — Processor Ranking Tests

These tests use synthetic processors and an illustrative
emission factor. They test the ranking logic, not real-world
environmental performance.
"""

import unittest

# Import the shipment and processor data structures.
from src.reserve.evaluation import Processor, Shipment

# Import the ranking function being tested.
from src.reserve.ranking import rank_eligible_processors


class TestProcessorRanking(unittest.TestCase):
    """Check ranking order and eligibility filtering."""

    def setUp(self):
        # Define one shipment shared by all ranking tests.
        self.shipment = Shipment(
            material="recycled_plastic",
            quantity_tonnes=10,
            required_quality=0.8,
            earliest_delivery_day=5,
            latest_delivery_day=8,
        )

        # This processor is eligible and is relatively close.
        self.near_processor = Processor(
            name="Near Processor",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=10,
        )

        # This processor is eligible but is farther away.
        self.far_processor = Processor(
            name="Far Processor",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=30,
        )

        # This processor is close but cannot handle the quantity.
        self.ineligible_processor = Processor(
            name="Insufficient Capacity",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=5,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=2,
        )

    def test_lower_emissions_rank_first(self):
        """The eligible processor with lower emissions ranks first."""
        results = rank_eligible_processors(
            self.shipment,
            [self.far_processor, self.near_processor],
            emission_factor_kg_per_tonne_km=0.1,
        )

        self.assertEqual(
            results[0]["processor"],
            "Near Processor",
        )
        self.assertEqual(
            results[1]["processor"],
            "Far Processor",
        )

    def test_ineligible_processor_is_excluded(self):
        """A processor failing capacity rules must not be ranked."""
        results = rank_eligible_processors(
            self.shipment,
            [
                self.ineligible_processor,
                self.near_processor,
            ],
            emission_factor_kg_per_tonne_km=0.1,
        )

        names = [result["processor"] for result in results]

        self.assertNotIn("Insufficient Capacity", names)
        self.assertIn("Near Processor", names)

    def test_empty_when_no_processor_is_eligible(self):
        """No eligible candidates should produce an empty ranking."""
        results = rank_eligible_processors(
            self.shipment,
            [self.ineligible_processor],
            emission_factor_kg_per_tonne_km=0.1,
        )

        self.assertEqual(results, [])

    def test_ties_are_sorted_by_name(self):
        """Equal estimates should use processor name consistently."""
        results = rank_eligible_processors(
            self.shipment,
            [self.far_processor, self.far_processor.__class__(
                name="Another Far Processor",
                accepted_materials=("recycled_plastic",),
                available_capacity_tonnes=15,
                quality_score=0.9,
                available_from_day=4,
                available_until_day=9,
                distance_km=30,
            )],
            emission_factor_kg_per_tonne_km=0.1,
        )

        self.assertEqual(
            [result["processor"] for result in results],
            ["Another Far Processor", "Far Processor"],
        )


# Run these tests directly when requested.
if __name__ == "__main__":
    unittest.main()
