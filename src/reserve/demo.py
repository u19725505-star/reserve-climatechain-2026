"""
RESERVE demonstration.

Demonstrates shipment eligibility, processor ranking, and estimated
transport emissions using fictional example data.

The data and emissions factor are illustrative, not verified
operational information or evidence of real-world climate benefits.
"""

from dataclasses import asdict
from pathlib import Path

from reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)
from reserve.ranking import rank_eligible_processors
from reserve.report import format_processor_report
from reserve.results import build_results_record, save_results_json
from reserve.demo_data import ILLUSTRATIVE_FACTOR, demo_processors


def main():
    """Run the complete RESERVE demonstration and save JSON results."""

    shipment = Shipment(
        material="recycled_plastic",
        quantity_tonnes=10.0,
        required_quality=0.8,
        earliest_delivery_day=5,
        latest_delivery_day=8,
    )

    processors = demo_processors()

    print("=" * 64)
    print("RESERVE — PROCESSOR SCREENING DEMONSTRATION")
    print("=" * 64)

    print("\nSHIPMENT")
    print(f"Material: {shipment.material}")
    print(f"Quantity: {shipment.quantity_tonnes:g} tonnes")
    print(f"Required quality: {shipment.required_quality:g}")
    print(
        f"Delivery window: days {shipment.earliest_delivery_day}"
        f"-{shipment.latest_delivery_day}"
    )

    print("\nELIGIBILITY CHECKS")
    for processor in processors:
        result = evaluate_processor(shipment, processor)

        if result.eligible:
            print(f"[ELIGIBLE] {processor.name}")
        else:
            print(f"[EXCLUDED] {processor.name}")
            for reason in result.reasons:
                print(f"    - {reason}")

    ranked = rank_eligible_processors(
        shipment=shipment,
        processors=processors,
        emission_factor_kg_per_tonne_km=emission_factor,
    )

    print("\nRANKED ELIGIBLE PROCESSORS")
    print("-" * 64)

    if not ranked:
        print("No eligible processors were found.")
    else:
        for position, candidate in enumerate(ranked, start=1):
            print(
                f"{position}. {candidate['processor']}: "
                f"{candidate['distance_km']:g} km, approximately "
                f"{candidate['estimated_emissions_kg_co2e']:g} kg CO2e"
            )

    print("\nFULL SCREENING REPORT")
    print(format_processor_report(ranked))

    # Save a machine-readable record of this comparison.
    shipment_record = asdict(shipment)
    shipment_record["accepted_processor_count"] = len(ranked)
    shipment_record["evaluated_processor_count"] = len(processors)

    record = build_results_record(
        shipment=shipment_record,
        ranked_candidates=ranked,
        emission_factor_kg_per_tonne_km=emission_factor,
        data_status="synthetic demonstration data",
    )

    output_path = Path("results") / "processor_comparison.json"
    saved_path = save_results_json(record, output_path)

    print("\nJSON RESULTS")
    print(f"Saved to: {saved_path.resolve()}")
    print(f"Ranked candidates recorded: {len(ranked)}")

    print("\nNOTES")
    print("- Shipment and processor details are fictional.")
    print("- The emissions factor is illustrative, not verified.")
    print("- The estimate covers transport only.")
    print("- No real-world emissions savings have been established.")
    print("=" * 64)


if __name__ == "__main__":
    main()
