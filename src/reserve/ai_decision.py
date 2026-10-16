"""Explainable decision-support scoring for RESERVE.

This is a transparent, deterministic multi-criteria decision model, not a
trained or validated machine-learning model. It only scores processors that
pass hard eligibility constraints. Scores are operational proxies and must
not be interpreted as measured climate benefit.
"""
from __future__ import annotations

from src.reserve.evaluation import Processor, Shipment, evaluate_processor


def score_eligible_processors(
    shipment: Shipment,
    processors: list[Processor],
    emission_factor_kg_per_tonne_km: float,
) -> dict:
    """Return explainable normalized scores for eligible candidates.

    The score combines four transparent criteria: lower modeled transport
    emissions (45%), quality margin (20%), capacity headroom (20%), and
    delivery-window overlap (15%). The weights are demonstration defaults,
    not empirically calibrated preferences.
    """
    eligible = [
        p for p in processors if evaluate_processor(shipment, p).eligible
    ]
    if not eligible:
        return {
            "model": "RESERVE-XAI-MCDM-0.1",
            "model_type": "transparent weighted multi-criteria decision model",
            "status": "no_eligible_candidates",
            "weights": {
                "transport_emissions": 0.45,
                "quality_margin": 0.20,
                "capacity_headroom": 0.20,
                "delivery_window_fit": 0.15,
            },
            "candidates": [],
            "limitations": [
                "Weights are illustrative and not trained on operational outcomes.",
                "Inputs use fictional demo profiles and an unsourced fallback factor.",
                "Scores are decision-support proxies, not verified climate outcomes.",
            ],
        }

    def factor_for(p):
        return (
            p.transport_emission_factor_kg_per_tonne_km
            if p.transport_emission_factor_kg_per_tonne_km is not None
            else emission_factor_kg_per_tonne_km
        )

    emissions = {
        p.name: p.distance_km * shipment.quantity_tonnes * factor_for(p)
        for p in eligible
    }
    min_e, max_e = min(emissions.values()), max(emissions.values())
    max_quality_margin = max(
        max(0.0, p.quality_score - shipment.required_quality) for p in eligible
    )
    max_headroom = max(
        max(0.0, p.available_capacity_tonnes - shipment.quantity_tonnes)
        for p in eligible
    )
    candidates = []
    for p in eligible:
        e = emissions[p.name]
        emission_score = 1.0 if max_e == min_e else (max_e - e) / (max_e - min_e)
        q_margin = max(0.0, p.quality_score - shipment.required_quality)
        quality_score = 1.0 if max_quality_margin == 0 else q_margin / max_quality_margin
        headroom = max(0.0, p.available_capacity_tonnes - shipment.quantity_tonnes)
        capacity_score = 1.0 if max_headroom == 0 else headroom / max_headroom
        overlap = max(
            0,
            min(p.available_until_day, shipment.latest_delivery_day)
            - max(p.available_from_day, shipment.earliest_delivery_day) + 1,
        )
        required_days = shipment.latest_delivery_day - shipment.earliest_delivery_day + 1
        delivery_score = min(1.0, overlap / max(1, required_days))
        components = {
            "transport_emissions": round(emission_score, 4),
            "quality_margin": round(quality_score, 4),
            "capacity_headroom": round(capacity_score, 4),
            "delivery_window_fit": round(delivery_score, 4),
        }
        total = (
            0.45 * emission_score
            + 0.20 * quality_score
            + 0.20 * capacity_score
            + 0.15 * delivery_score
        )
        candidates.append({
            "processor": p.name,
            "score": round(total, 4),
            "score_percent": round(total * 100, 1),
            "estimated_transport_emissions_kg_co2e": round(e, 2),
            "criteria": components,
            "explanation": (
                "Eligible candidate; score balances modeled transport emissions, "
                "quality margin, capacity headroom, and delivery-window fit."
            ),
        })
    candidates.sort(key=lambda x: (-x["score"], x["processor"]))
    for rank, item in enumerate(candidates, 1):
        item["ai_rank"] = rank
    return {
        "model": "RESERVE-XAI-MCDM-0.1",
        "model_type": "transparent weighted multi-criteria decision model",
        "status": "advisory_only",
        "weights": {
            "transport_emissions": 0.45,
            "quality_margin": 0.20,
            "capacity_headroom": 0.20,
            "delivery_window_fit": 0.15,
        },
        "candidates": candidates,
        "limitations": [
            "Weights are illustrative and not trained or calibrated on operational outcomes.",
            "Inputs use fictional demo profiles and an unsourced fallback factor.",
            "Scores are decision-support proxies, not verified climate outcomes.",
            "Hard eligibility rules take precedence over all scores.",
        ],
    }
