"""
RESERVE — Eligibility Demonstration

Runs one example shipment against two candidate processors.
The example uses illustrative data, not real facility records.
"""

# Import the project models and eligibility rule.
from src.reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)


def main():
    """Evaluate two illustrative processors and print the results."""

    # Define the shipment's material, quantity, quality, and timing needs.
    shipment = Shipment(
        material="recycled_plastic",
        quantity_tonnes=10,
        required_quality=0.8,
        earliest_delivery_day=5,
        latest_delivery_day=8,
    )

    # Candidate A has enough capacity and meets the other requirements.
    candidate_a = Processor(
        name="Processor A",
        accepted_materials=("recycled_plastic",),
        available_capacity_tonnes=15,
        quality_score=0.9,
        available_from_day=4,
        available_until_day=9,
        distance_km=25,
    )

    # Candidate B accepts the material but lacks sufficient capacity.
    candidate_b = Processor(
        name="Processor B",
        accepted_materials=("recycled_plastic",),
        available_capacity_tonnes=5,
        quality_score=0.9,
        available_from_day=4,
        available_until_day=9,
        distance_km=40,
    )

    # Evaluate each candidate using the same transparent rules.
    for candidate in (candidate_a, candidate_b):
        result = evaluate_processor(shipment, candidate)

        # Display the decision and the reasons behind it.
        status = "ELIGIBLE" if result.eligible else "NOT ELIGIBLE"
        print(f"\n{result.processor}: {status}")

        if result.reasons:
            for reason in result.reasons:
                print(f"  - {reason}")
        else:
            print("  - All eligibility rules passed.")


# Run the demonstration when this file is executed directly.
if __name__ == "__main__":
    main()
