"""
RESERVE — Transport Emissions Tests

Checks the emissions formula and its input validation.
All values are illustrative test data, not measured emissions.
"""

import unittest

# Import the transport emissions calculation.
from src.reserve.emissions import estimate_transport_emissions_kg


class TestTransportEmissions(unittest.TestCase):
    """Verify transport estimates and reject invalid inputs."""

    def test_basic_calculation(self):
        # 25 km × 10 tonnes × 0.1 kg CO2e per tonne-km = 25 kg.
        result = estimate_transport_emissions_kg(
            distance_km=25,
            quantity_tonnes=10,
            emission_factor_kg_per_tonne_km=0.1,
        )
        self.assertAlmostEqual(result, 25.0)

    def test_longer_distance_increases_emissions(self):
        # Holding the shipment and factor constant, twice the distance
        # should produce twice the estimated emissions.
        short_trip = estimate_transport_emissions_kg(10, 10, 0.1)
        long_trip = estimate_transport_emissions_kg(20, 10, 0.1)

        self.assertAlmostEqual(long_trip, short_trip * 2)

    def test_zero_quantity_is_rejected(self):
        # Zero tonnes is not a valid shipment quantity.
        with self.assertRaises(ValueError):
            estimate_transport_emissions_kg(10, 0, 0.1)

    def test_negative_distance_is_rejected(self):
        # Distances must not be negative.
        with self.assertRaises(ValueError):
            estimate_transport_emissions_kg(-10, 10, 0.1)

    def test_negative_factor_is_rejected(self):
        # An invalid negative factor must not silently produce
        # a misleading emissions estimate.
        with self.assertRaises(ValueError):
            estimate_transport_emissions_kg(10, 10, -0.1)


# Allow this test file to be run directly as well.
if __name__ == "__main__":
    unittest.main()
