"""RESERVE: interactive supply-chain screening demonstration."""
from pathlib import Path
import math
import sys

from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from src.reserve.evaluation import Processor, Shipment, evaluate_processor
from src.reserve.ranking import rank_eligible_processors

app = Flask(__name__)

ILLUSTRATIVE_FACTOR = 0.1


def demo_processors():
    """Fictional processors for a repeatable interactive demonstration."""
    return [
        Processor(
            name="Processor A",
            accepted_materials=("recycled_plastic", "paper"),
            available_capacity_tonnes=25,
            quality_score=0.92,
            available_from_day=1,
            available_until_day=18,
            distance_km=25,
        ),
        Processor(
            name="Processor B",
            accepted_materials=("recycled_plastic",),
            available_capacity_tonnes=18,
            quality_score=0.86,
            available_from_day=3,
            available_until_day=12,
            distance_km=15,
        ),
        Processor(
            name="Processor C",
            accepted_materials=("recycled_plastic", "paper", "glass"),
            available_capacity_tonnes=6,
            quality_score=0.95,
            available_from_day=1,
            available_until_day=20,
            distance_km=8,
        ),
        Processor(
            name="Processor D",
            accepted_materials=("wood",),
            available_capacity_tonnes=40,
            quality_score=0.98,
            available_from_day=1,
            available_until_day=20,
            distance_km=32,
        ),
    ]


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "RESERVE demo"})


@app.post("/api/evaluate")
def evaluate():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    try:
        material = str(data.get("material", "recycled_plastic"))
        quantity = float(data.get("quantity_tonnes", 10))
        quality = float(data.get("required_quality", 0.8))
        earliest = int(data.get("earliest_delivery_day", 5))
        latest = int(data.get("latest_delivery_day", 8))
    except (TypeError, ValueError):
        return jsonify({"error": "Enter valid numeric shipment requirements."}), 400

    if material not in {"recycled_plastic", "paper", "glass", "wood"}:
        return jsonify({"error": "Select a supported demonstration material."}), 400
    if not math.isfinite(quantity) or quantity <= 0:
        return jsonify({"error": "Quantity must be a finite number greater than zero."}), 400
    if not math.isfinite(quality) or not 0 <= quality <= 1:
        return jsonify({"error": "Quality must be a finite number between 0 and 1."}), 400
    if earliest < 0 or latest < earliest:
        return jsonify({"error": "Delivery days must be non-negative and ordered."}), 400

    shipment = Shipment(
        material=material,
        quantity_tonnes=quantity,
        required_quality=quality,
        earliest_delivery_day=earliest,
        latest_delivery_day=latest,
    )
    processors = demo_processors()
    evaluations = {
        p.name: evaluate_processor(shipment, p) for p in processors
    }

    ranked = rank_eligible_processors(
        shipment, processors, ILLUSTRATIVE_FACTOR
    )

    all_processors = []
    for processor in processors:
        result = evaluations[processor.name]
        all_processors.append({
            "name": processor.name,
            "distance_km": processor.distance_km,
            "capacity_tonnes": processor.available_capacity_tonnes,
            "quality_score": processor.quality_score,
            "accepted_materials": list(processor.accepted_materials),
            "eligible": bool(result.eligible),
            "reasons": list(result.reasons),
            "estimated_emissions_kg_co2e": round(
                processor.distance_km
                * quantity
                * (
                    processor.transport_emission_factor_kg_per_tonne_km
                    if processor.transport_emission_factor_kg_per_tonne_km is not None
                    else ILLUSTRATIVE_FACTOR
                ),
                2,
            ),
            "emission_factor_kg_per_tonne_km": (
                processor.transport_emission_factor_kg_per_tonne_km
                if processor.transport_emission_factor_kg_per_tonne_km is not None
                else ILLUSTRATIVE_FACTOR
            ),
            "emission_factor_source": (
                processor.transport_emission_factor_source
                if processor.transport_emission_factor_kg_per_tonne_km is not None
                else "Illustrative fallback factor; not a sourced processor value"
            ),
        })

    ranked_names = [str(candidate["processor"]) for candidate in ranked]
    rank_lookup = {name: index + 1 for index, name in enumerate(ranked_names)}
    for item in all_processors:
        item["rank"] = rank_lookup.get(item["name"])

    # Fair operational comparison: baseline must satisfy the same shipment
    # constraints. The nearest overall processor is shown separately.
    nearest = min(processors, key=lambda p: (p.distance_km, p.name))
    eligible_processors = [
        p for p in processors if evaluations[p.name].eligible
    ]
    baseline_processor = (
        min(eligible_processors, key=lambda p: (p.distance_km, p.name))
        if eligible_processors
        else None
    )
    nearest_result = evaluations[nearest.name]
    selected_processor = next(
        (p for p in processors if ranked_names and p.name == ranked_names[0]),
        None,
    )
    baseline_emissions = (
        baseline_processor.distance_km * quantity
        * (
            baseline_processor.transport_emission_factor_kg_per_tonne_km
            if baseline_processor.transport_emission_factor_kg_per_tonne_km is not None
            else ILLUSTRATIVE_FACTOR
        )
        if baseline_processor is not None else None
    )
    selected_emissions = (
        selected_processor.distance_km * quantity
        * (
            selected_processor.transport_emission_factor_kg_per_tonne_km
            if selected_processor.transport_emission_factor_kg_per_tonne_km is not None
            else ILLUSTRATIVE_FACTOR
        )
        if selected_processor is not None else None
    )
    absolute_difference = (
        baseline_emissions - selected_emissions
        if baseline_emissions is not None and selected_emissions is not None
        else None
    )
    percent_difference = (
        (absolute_difference / baseline_emissions) * 100
        if baseline_emissions not in (None, 0) and absolute_difference is not None
        else None
    )

    return jsonify({
        "shipment": {
            "material": material,
            "quantity_tonnes": quantity,
            "required_quality": quality,
            "earliest_delivery_day": earliest,
            "latest_delivery_day": latest,
        },
        "processors": all_processors,
        "ranked_processor_names": ranked_names,
        "selected": ranked_names[0] if ranked_names else None,
        "eligible_count": len(ranked),
        "excluded_count": len(processors) - len(ranked),
        "baseline": {
            "processor": baseline_processor.name if baseline_processor else None,
            "eligible": bool(baseline_processor is not None),
            "method": "nearest eligible processor under the same shipment constraints",
            "estimated_emissions_kg_co2e": (
                round(baseline_emissions, 2)
                if baseline_emissions is not None else None
            ),
            "reasons": [],
        },
        "nearest_overall_processor": {
            "processor": nearest.name,
            "eligible": bool(nearest_result.eligible),
            "reasons": list(nearest_result.reasons),
        },
        "comparison": {
            "selected_processor": selected_processor.name if selected_processor else None,
            "selected_estimated_emissions_kg_co2e": (
                round(selected_emissions, 2)
                if selected_emissions is not None else None
            ),
            "baseline_estimated_emissions_kg_co2e": (
                round(baseline_emissions, 2)
                if baseline_emissions is not None else None
            ),
            "estimated_avoided_kg_co2e": (
                round(absolute_difference, 2)
                if absolute_difference is not None else None
            ),
            "estimated_reduction_percent": (
                round(percent_difference, 2)
                if percent_difference is not None else None
            ),
            "interpretation": (
                "Modeled comparison only; not measured or verified climate impact."
            ),
        },
        "emissions_factor": ILLUSTRATIVE_FACTOR,
        "emissions_status": "Illustrative screening estimate, not verified measurement",
        "data_status": "Fictional demonstration data",
        "climate_impact_claim": (
            "No verified emissions reduction or real-world climate benefit "
            "is established by this demonstration."
        ),
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
