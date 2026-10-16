"""
RESERVE — Processor Eligibility Evaluation

Checks whether a processor can handle a proposed shipment.
This module checks eligibility only; ranking and emissions
calculations will be added later.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Shipment:
    """Requirements for a proposed shipment."""

    material: str
    quantity_tonnes: float
    required_quality: float
    earliest_delivery_day: int
    latest_delivery_day: int


@dataclass(frozen=True)
class Processor:
    """Capabilities and availability of a candidate processor."""

    name: str
    accepted_materials: tuple[str, ...]
    available_capacity_tonnes: float
    quality_score: float
    available_from_day: int
    available_until_day: int
    distance_km: float


@dataclass(frozen=True)
class Evaluation:
    """Decision and explanations for a processor."""

    processor: str
    eligible: bool
    reasons: tuple[str, ...]


def evaluate_processor(
    shipment: Shipment,
    processor: Processor,
) -> Evaluation:
    """Check each eligibility rule and explain any failures."""

    # Store all failed rules so decisions remain explainable.
    reasons = []

    # A shipment must have a positive quantity.
    if shipment.quantity_tonnes <= 0:
        reasons.append("Shipment quantity must be positive.")

    # The delivery window must start before it ends.
    if shipment.earliest_delivery_day > shipment.latest_delivery_day:
        reasons.append("Shipment delivery window is invalid.")

    # The processor must accept the shipment's material.
    if shipment.material not in processor.accepted_materials:
        reasons.append("Processor does not accept this material.")

    # The processor must have enough available capacity.
    if processor.available_capacity_tonnes < shipment.quantity_tonnes:
        reasons.append("Insufficient available processing capacity.")

    # The processor must meet the required quality score.
    if processor.quality_score < shipment.required_quality:
        reasons.append("Processor quality score is below the requirement.")

    # Processor availability must overlap the delivery window.
    if (
        processor.available_until_day < shipment.earliest_delivery_day
        or processor.available_from_day > shipment.latest_delivery_day
    ):
        reasons.append("Processor is unavailable during the delivery window.")

    # A negative distance is invalid.
    if processor.distance_km < 0:
        reasons.append("Processor distance cannot be negative.")

    # Eligibility is true only when every rule passes.
    return Evaluation(
        processor=processor.name,
        eligible=len(reasons) == 0,
        reasons=tuple(reasons),
    )
