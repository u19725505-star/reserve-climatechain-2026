# Emissions Method

## Purpose
The prototype exposes a simple transport-emissions estimate so reviewers can inspect the inputs and assumptions. It is a screening calculation, not a measured inventory or independently verified footprint.

## Basic calculation
Where the configured factor is expressed per tonne-kilometre:

`Estimated emissions (kg CO₂e) = shipment mass (tonnes) × route distance (km) × emissions factor (kg CO₂e / tonne-km)`

The implementation's units and any conversions should be checked alongside the code and input data before reusing the calculation outside the demo.

## Current default
The fallback factor is `0.1 kg CO₂e/(tonne-km)`. It is illustrative and unsourced; it is not an EPA factor and should not be presented as an authoritative value.

## Baseline
The comparison baseline is the nearest processor that satisfies the same shipment constraints. The nearest processor overall may be ineligible and is shown separately. If every candidate uses the same emissions factor, the estimate varies only with mass and distance; for the same shipment mass, ranking by estimated emissions is therefore equivalent to ranking by distance. Under that condition, the nearest-eligible baseline should produce 0% modeled improvement unless defensible candidate-specific factors alter the comparison.

## Interpretation
- A modeled estimate is not a measurement.
- A modeled difference is not proof of an actual emissions reduction.
- The current fictional processor profiles do not establish real routes, loads, vehicle types, empty running, or actual emissions.
- Do not claim verified climate savings from the demo.

## Requirements before a pilot
For every factor, record:
1. source organization and exact citation;
2. publication or dataset year and access date;
3. freight mode, vehicle/fuel category, geography, and load assumptions;
4. original units and conversion method;
5. system boundary and gases included;
6. treatment of empty running and allocation;
7. uncertainty, exclusions, and applicability limits.

Replace the fallback with traceable, scenario-appropriate factors and independently review the methodology before reporting real-world outcomes.
