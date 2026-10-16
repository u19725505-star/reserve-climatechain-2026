"""
RESERVE — Processor Evaluation Tests

These tests check that the eligibility rules return the
expected result for suitable and unsuitable processors.
"""

import unittest

# Import the data structures and evaluation function being tested.
from src.reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)


class TestProcessorEvaluation(unittest.TestCase):
    """Test processor eligibility under different conditions."""

    def setUp(self):
        # Reuse one valid shipment across the test cases.
        self.shipment = Shipment(
            material="recycled_plastic",
            quantity_tonnes=10,
            required_quality=0.8,
            earliest_delivery_day=5,
            latest_delivery_day=8,
        )

        # This processor meets all shipment requirements.
        self.processor = Processor(
            name="Processor A",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=25,
        )

    def test_eligible_processor(self):
        """A processor meeting all rules should be eligible."""
        result = evaluate_processor(self.shipment, self.processor)

        self.assertTrue(result.eligible)
        self.assertEqual(result.reasons, ())

    def test_insufficient_capacity(self):
        """A processor without enough capacity should be rejected."""
        processor = Processor(
            name="Processor B",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=5,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=25,
        )

        result = evaluate_processor(self.shipment, processor)

        self.assertFalse(result.eligible)
        self.assertIn(
            "Insufficient available processing capacity.",
            result.reasons,
        )

    def test_wrong_material(self):
        """A processor that rejects the material should be rejected."""
        processor = Processor(
            name="Processor C",
            accepted_materials=("wood",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=25,
        )

        result = evaluate_processor(self.shipment, processor)

        self.assertFalse(result.eligible)
        self.assertIn(
            "Processor does not accept this material.",
            result.reasons,
        )

    def test_delivery_window_mismatch(self):
        """A processor unavailable in time should be rejected."""
        processor = Processor(
            name="Processor D",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15,
            quality_score=0.9,
            available_from_day=10,
            available_until_day=12,
            distance_km=25,
        )

        result = evaluate_processor(self.shipment, processor)

        self.assertFalse(result.eligible)
        self.assertIn(
            "Processor is unavailable during the delivery window.",
            result.reasons,
        )


# Run the tests when this file is executed directly.
if __name__ == "__main__":
    unittest.main()
