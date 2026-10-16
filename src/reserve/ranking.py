"""
RESERVE — Eligible Processor Ranking

Purpose:
    Rank processors that pass the shipment eligibility rules.

Method:
    1. Evaluate each processor against the shipment requirements.
    2. Exclude processors that fail eligibility.
    3. Estimate transport emissions for eligible processors.
    4. Rank the remaining candidates from lowest to highest
       estimated transport emissions.

The ranking uses an illustrative emission factor supplied by
the caller. It does not claim that estimates are measured values.
"""

# Import the eligibility checks and emissions calculation.
from src.reserve.evaluation import (
    Processor,
    Shipment,
    evaluate_processor,
)
from src.reserve.emissions import estimate_transport_emissions_kg


def rank_eligible_processors(
    shipment: Shipment,
    processors: list[Processor],
    emission_factor_kg_per_tonne_km: float,
) -> list[dict]:
    """
    Return eligible processors ordered by estimated emissions.

    Each result includes the processor name, distance, estimated
    emissions, and eligibility reasons.

    Ineligible processors are excluded from the ranked results.
    """

    # Store eligible candidates and their calculated estimates.
    ranked_candidates = []

    # Evaluate every processor against the shipment requirements.
    for processor in processors:
        evaluation = evaluate_processor(shipment, processor)

        # Never rank a processor that fails an eligibility rule.
        if not evaluation.eligible:
            continue

        # Estimate emissions using the supplied factor.
        emissions = estimate_transport_emissions_kg(
            distance_km=processor.distance_km,
            quantity_tonnes=shipment.quantity_tonnes,
            emission_factor_kg_per_tonne_km=(
                emission_factor_kg_per_tonne_km
            ),
        )

        # Keep the information needed to explain the ranking.
        ranked_candidates.append(
            {
                "processor": processor.name,
                "distance_km": processor.distance_km,
                "estimated_emissions_kg_co2e": emissions,
                "eligible": True,
                "reasons": evaluation.reasons,
            }
        )

    # Sort from the lowest estimated emissions to the highest.
    # Processor name breaks ties consistently.
    ranked_candidates.sort(
        key=lambda candidate: (
            candidate["estimated_emissions_kg_co2e"],
            candidate["processor"],
        )
    )

    return ranked_candidates
