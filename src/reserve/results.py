"""Structured JSON output for RESERVE processor comparisons."""

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any, Mapping, Sequence


def build_results_record(
    *,
    shipment: Mapping[str, Any],
    ranked_candidates: Sequence[Mapping[str, Any]],
    emission_factor_kg_per_tonne_km: float,
    data_status: str = "synthetic demonstration data",
) -> dict[str, Any]:
    """Build a JSON-serializable processor comparison record."""

    if emission_factor_kg_per_tonne_km < 0:
        raise ValueError("Emission factor cannot be negative.")

    processors = []

    for rank, candidate in enumerate(ranked_candidates, start=1):
        processors.append(
            {
                "rank": rank,
                "processor": str(candidate["processor"]),
                "eligible": bool(candidate.get("eligible", True)),
                "distance_km": float(candidate["distance_km"]),
                "estimated_emissions_kg_co2e": float(
                    candidate["estimated_emissions_kg_co2e"]
                ),
                "reasons": list(candidate.get("reasons", [])),
            }
        )

    return {
        "schema_version": "1.0",
        "project": "RESERVE",
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "shipment": dict(shipment),
        "ranking_method": "ascending estimated transport emissions",
        "emissions": {
            "emission_factor_kg_per_tonne_km": float(
                emission_factor_kg_per_tonne_km
            ),
            "status": "screening estimate, not verified measurement",
        },
        "data_status": data_status,
        "climate_impact_claim": (
            "No verified emissions reduction or real-world climate benefit "
            "is established by this record."
        ),
        "ranked_processors": processors,
    }


def save_results_json(
    record: Mapping[str, Any],
    output_path: str | Path,
) -> Path:
    """Save a record as formatted JSON and return its path."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file:
        json.dump(record, file, indent=2, ensure_ascii=False)
        file.write("\n")

    return path
