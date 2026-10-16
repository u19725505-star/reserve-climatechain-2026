"""
RESERVE demonstration.

Demonstrates shipment eligibility, processor ranking, and estimated
transport emissions using fictional example data.

The data and emissions factor are illustrative, not verified
operational information or evidence of real-world climate benefits.
"""

from reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)
from reserve.ranking import rank_eligible_processors
from reserve.report import format_processor_report


def main():
    """Run the complete RESERVE demonstration."""

    # Define a fictional shipment using the existing Shipment fields.
    shipment = Shipment(
        material="recycled_plastic",
        quantity_tonnes=10.0,
        required_quality=0.8,
        earliest_delivery_day=5,
        latest_delivery_day=8,
    )

    # Define fictional processors using the existing Processor fields.
    processors = [
        Processor(
            name="Processor A",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=20.0,
            quality_score=0.9,
            available_from_day=4,
            available_until_day=9,
            distance_km=25.0,
        ),
        Processor(
            name="Processor B",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=15.0,
            quality_score=0.85,
            available_from_day=5,
            available_until_day=8,
            distance_km=15.0,
        ),
        Processor(
            name="Processor C",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=5.0,
            quality_score=0.95,
            available_from_day=5,
            available_until_day=8,
            distance_km=5.0,
        ),
        Processor(
            name="Processor D",
            accepted_materials=("wood",),
            available_capacity_tonnes=20.0,
            quality_score=0.95,
            available_from_day=5,
            available_until_day=8,
            distance_km=10.0,
        ),
    ]

    # Illustrative factor only: 0.1 kg CO2e per tonne-kilometre.
    # Use a documented, appropriate factor for any real application.
    emission_factor = 0.1

    print("=" * 64)
    print("RESERVE — PROCESSOR SCREENING DEMONSTRATION")
    print("=" * 64)

    # Print the shipment requirements.
    print("\nSHIPMENT")
    print(f"Material: {shipment.material}")
    print(f"Quantity: {shipment.quantity_tonnes:g} tonnes")
    print(f"Required quality: {shipment.required_quality:g}")
    print(
        f"Delivery window: days {shipment.earliest_delivery_day}"
        f"-{shipment.latest_delivery_day}"
    )

    # Show the eligibility decision and reasons for each processor.
    print("\nELIGIBILITY CHECKS")
    for processor in processors:
        result = evaluate_processor(shipment, processor)

        if result.eligible:
            print(f"[ELIGIBLE] {processor.name}")
        else:
            print(f"[EXCLUDED] {processor.name}")
            for reason in result.reasons:
                print(f"    - {reason}")

    # Rank eligible processors using the existing ranking module.
    ranked = rank_eligible_processors(
        shipment=shipment,
        processors=processors,
        emission_factor_kg_per_tonne_km=emission_factor,
    )

    # The ranking module returns the processor name as a string.
    print("\nRANKED ELIGIBLE PROCESSORS")
    print("-" * 64)

    if not ranked:
        print("No eligible processors were found.")
    else:
        for position, candidate in enumerate(ranked, start=1):
            processor_name = candidate["processor"]
            distance = candidate["distance_km"]
            emissions = candidate["estimated_emissions_kg_co2e"]

            print(
                f"{position}. {processor_name}: "
                f"{distance:g} km, approximately "
                f"{emissions:g} kg CO2e"
            )

    # Print the project's existing formatted screening report.
    print("\nFULL SCREENING REPORT")
    print(format_processor_report(ranked))

    # Explain the limitations of this demonstration.
    print("\nNOTES")
    print("- Shipment and processor details are fictional.")
    print("- The emissions factor is illustrative, not verified.")
    print("- The estimate covers transport only.")
    print("- No real-world emissions savings have been established.")
    print("=" * 64)


if __name__ == "__main__":
    main()
