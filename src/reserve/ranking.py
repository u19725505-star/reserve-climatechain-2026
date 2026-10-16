"""
RESERVE — Eligibility-constrained transport-emissions ranking.

If a processor has a documented candidate-specific factor, use it.
Otherwise use the caller-supplied fallback factor, which must be
labelled illustrative unless its provenance has been verified.
"""
from src.reserve.evaluation import Processor, Shipment, evaluate_processor
from src.reserve.emissions import estimate_transport_emissions_kg


def rank_eligible_processors(
    shipment: Shipment,
    processors: list[Processor],
    emission_factor_kg_per_tonne_km: float,
) -> list[dict]:
    """Rank only eligible processors by estimated transport emissions."""
    ranked_candidates = []
    for processor in processors:
        evaluation = evaluate_processor(shipment, processor)
        if not evaluation.eligible:
            continue

        candidate_factor = processor.transport_emission_factor_kg_per_tonne_km
        factor = (
            candidate_factor
            if candidate_factor is not None
            else emission_factor_kg_per_tonne_km
        )
        emissions = estimate_transport_emissions_kg(
            distance_km=processor.distance_km,
            quantity_tonnes=shipment.quantity_tonnes,
            emission_factor_kg_per_tonne_km=factor,
        )
        ranked_candidates.append({
            "processor": processor.name,
            "distance_km": processor.distance_km,
            "estimated_emissions_kg_co2e": emissions,
            "emission_factor_kg_per_tonne_km": factor,
            "emission_factor_source": (
                processor.transport_emission_factor_source
                if candidate_factor is not None
                else "Illustrative fallback factor supplied by caller"
            ),
            "emission_factor_url": processor.transport_emission_factor_url,
            "eligible": True,
            "reasons": evaluation.reasons,
        })

    ranked_candidates.sort(key=lambda candidate: (
        candidate["estimated_emissions_kg_co2e"],
        candidate["processor"],
    ))
    return ranked_candidates
