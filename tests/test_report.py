"""
RESERVE — Comparison Report Tests

Checks that processor rankings are presented clearly,
including the case where no candidate qualifies.
"""

import unittest

# Import the report formatter.
from src.reserve.report import format_processor_report


class TestProcessorReport(unittest.TestCase):
    """Verify report headings, values, and empty-result handling."""

    def test_report_contains_processor_details(self):
        """The report should show processor names and estimates."""
        candidates = [
            {
                "processor": "Processor A",
                "distance_km": 10.0,
                "estimated_emissions_kg_co2e": 10.0,
                "eligible": True,
                "reasons": (),
            },
            {
                "processor": "Processor B",
                "distance_km": 30.0,
                "estimated_emissions_kg_co2e": 30.0,
                "eligible": True,
                "reasons": (),
            },
        ]

        report = format_processor_report(candidates)

        self.assertIn("RESERVE Processor Comparison", report)
        self.assertIn("Processor A", report)
        self.assertIn("Processor B", report)
        self.assertIn("10.00", report)
        self.assertIn("30.00", report)
        self.assertIn("screening estimates", report)

    def test_lower_emissions_candidate_appears_first(self):
        """The report should preserve the supplied ranking order."""
        candidates = [
            {
                "processor": "Lower Emissions",
                "distance_km": 10.0,
                "estimated_emissions_kg_co2e": 10.0,
                "eligible": True,
                "reasons": (),
            },
            {
                "processor": "Higher Emissions",
                "distance_km": 30.0,
                "estimated_emissions_kg_co2e": 30.0,
                "eligible": True,
                "reasons": (),
            },
        ]

        report = format_processor_report(candidates)

        self.assertLess(
            report.index("Lower Emissions"),
            report.index("Higher Emissions"),
        )

    def test_empty_ranking_has_clear_message(self):
        """The report should explain when no candidate qualifies."""
        report = format_processor_report([])

        self.assertIn("No eligible processors were found", report)


# Allow these tests to run directly.
if __name__ == "__main__":
    unittest.main()
