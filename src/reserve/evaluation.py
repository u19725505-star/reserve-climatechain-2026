"""
RESERVE — Processor Eligibility Evaluation

Checks whether a processor can handle a proposed shipment.
Transport emissions inputs are optional and are used by ranking
when they are supplied with explicit source provenance.
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
    """Capabilities, availability, and optional sourced transport intensity.

    transport_emission_factor_kg_per_tonne_km must be expressed in
    kg CO2e per tonne-kilometre. When supplied, the source label must
    identify the evidence behind that value. The value is not assumed
    to be a facility's own measured factor unless its source says so.
    """

    name: str
    accepted_materials: tuple[str, ...]
    available_capacity_tonnes: float
    quality_score: float
    available_from_day: int
    available_until_day: int
    distance_km: float
    transport_emission_factor_kg_per_tonne_km: float | None = None
    transport_emission_factor_source: str | None = None
    transport_emission_factor_url: str | None = None

    def __post_init__(self):
        factor = self.transport_emission_factor_kg_per_tonne_km
        source = self.transport_emission_factor_source
        if factor is not None and factor < 0:
            raise ValueError("Processor emissions factor cannot be negative.")
        if factor is not None and not (source and source.strip()):
            raise ValueError(
                "A processor-specific emissions factor requires a source label."
            )


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

    reasons = []

    if shipment.quantity_tonnes <= 0:
        reasons.append("Shipment quantity must be positive.")

    if shipment.earliest_delivery_day > shipment.latest_delivery_day:
        reasons.append("Shipment delivery window is invalid.")

    if shipment.material not in processor.accepted_materials:
        reasons.append("Processor does not accept this material.")

    if processor.available_capacity_tonnes < shipment.quantity_tonnes:
        reasons.append("Insufficient available processing capacity.")

    if processor.quality_score < shipment.required_quality:
        reasons.append("Processor quality score is below the requirement.")

    if (
        processor.available_until_day < shipment.earliest_delivery_day
        or processor.available_from_day > shipment.latest_delivery_day
    ):
        reasons.append("Processor is unavailable during the delivery window.")

    if processor.distance_km < 0:
        reasons.append("Processor distance cannot be negative.")

    return Evaluation(
        processor=processor.name,
        eligible=len(reasons) == 0,
        reasons=tuple(reasons),
    )
