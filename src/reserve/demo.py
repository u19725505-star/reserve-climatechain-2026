"""
RESERVE — Processor Eligibility and Emissions Demonstration

Purpose:
    Evaluate two illustrative processors and estimate the
    transport emissions associated with each candidate.

All processor data and the emissions factor below are synthetic
demonstration values, not real-world facility measurements.
"""

# Import the processor eligibility models and evaluation function.
from src.reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)

# Import the transport emissions calculation.
from src.reserve.emissions import estimate_transport_emissions_kg


def main():
    """Evaluate candidate processors and display their results."""

    # Define the shipment requirements.
    shipment = Shipment(
        material="recycled_plastic",
        quantity_tonnes=10,
        required_quality=0.8,
        earliest_delivery_day=5,
        latest_delivery_day=8,
    )

    # Candidate A meets the eligibility requirements.
    candidate_a = Processor(
        name="Processor A",
        accepted_materials=("recycled_plastic",),
        available_capacity_tonnes=15,
        quality_score=0.9,
        available_from_day=4,
        available_until_day=9,
        distance_km=25,
    )

    # Candidate B accepts the material but lacks enough capacity.
    candidate_b = Processor(
        name="Processor B",
        accepted_materials=("recycled_plastic",),
        available_capacity_tonnes=5,
        quality_score=0.9,
        available_from_day=4,
        available_until_day=9,
        distance_km=40,
    )

    # Illustrative factor for testing the calculation only.
    # Replace this with a documented factor before real use.
    example_emission_factor = 0.1

    # Evaluate each candidate and explain the decision.
    for candidate in (candidate_a, candidate_b):
        result = evaluate_processor(shipment, candidate)

        # Print the eligibility decision first.
        status = "ELIGIBLE" if result.eligible else "NOT ELIGIBLE"
        print(f"\n{result.processor}: {status}")

        # Show the reasons when a candidate fails a rule.
        if result.reasons:
            for reason in result.reasons:
                print(f"  - {reason}")
        else:
            print("  - All eligibility rules passed.")

        # Calculate and display the screening estimate.
        # This is not proof of actual transport emissions.
        emissions = estimate_transport_emissions_kg(
            distance_km=candidate.distance_km,
            quantity_tonnes=shipment.quantity_tonnes,
            emission_factor_kg_per_tonne_km=example_emission_factor,
        )

        print(f"  Illustrative transport estimate: {emissions:.2f} kg CO2e")

        # Explain that eligibility and emissions are separate checks.
        if not result.eligible:
            print("  Note: emissions are shown for comparison only;")
            print("        this candidate currently fails eligibility.")


# Run the demonstration when this module is executed directly.
if __name__ == "__main__":
    main()
