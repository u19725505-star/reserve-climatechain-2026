"""
RESERVE — Transport Emissions Estimation

Purpose:
    Estimate transport emissions for a material shipment.

Important:
    This is a simple screening estimate, not a verified
    greenhouse-gas inventory. The emission factor is supplied
    by the caller and must be replaced with a documented,
    appropriate factor before making real-world claims.
"""


def estimate_transport_emissions_kg(
    distance_km: float,
    quantity_tonnes: float,
    emission_factor_kg_per_tonne_km: float,
) -> float:
    """
    Estimate transport emissions in kilograms of CO2-equivalent.

    Formula:
        emissions = distance × shipment tonnes × emission factor

    The factor's units are kg CO2e per tonne-kilometre.

    Args:
        distance_km: One-way transport distance in kilometres.
        quantity_tonnes: Shipment mass in metric tonnes.
        emission_factor_kg_per_tonne_km: Assumed transport factor.

    Returns:
        Estimated emissions in kg CO2e.

    Raises:
        ValueError: If any input is negative or the shipment mass
                    is not positive.
    """

    # Distance and the emission factor cannot be negative.
    if distance_km < 0:
        raise ValueError("Distance cannot be negative.")

    if emission_factor_kg_per_tonne_km < 0:
        raise ValueError("Emission factor cannot be negative.")

    # A shipment must have a positive mass.
    if quantity_tonnes <= 0:
        raise ValueError("Shipment quantity must be positive.")

    # Calculate the estimated transport emissions.
    return (
        distance_km
        * quantity_tonnes
        * emission_factor_kg_per_tonne_km
    )
