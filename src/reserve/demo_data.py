"""Single source of truth for fictional RESERVE demo processor profiles."""

from reserve.evaluation import Processor

# Illustrative fallback only; this is not a sourced freight emissions factor.
ILLUSTRATIVE_FACTOR = 0.1


def demo_processors():
    """Return the common fictional processor profiles used by the web and CLI demos."""
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
