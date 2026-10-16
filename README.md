# RESERVE — ClimateChain 2026

**AI-assisted processing reservations and auditable supply-chain decisions**

RESERVE is a prototype designed to help organizations evaluate potential material-processing destinations before dispatch. It combines processor acceptance requirements, available capacity, transport considerations, and documented reservation decisions in a single workflow.

## The problem

A suitable processor may not be available when a shipment arrives. Material-quality uncertainty, capacity constraints, scheduling changes, and transport requirements can make routing decisions difficult to coordinate and audit.

## Our approach

RESERVE is designed to support:

* **Processor matching:** evaluate candidate processors against material and operational requirements.
* **Conditional reservations:** record proposed processing commitments and their status.
* **Disruption handling:** document cancellations, changes, and potential reallocation.
* **Emissions accounting:** estimate transport-related emissions using documented assumptions and emission factors.
* **Auditability:** maintain a linked record of reservation events and changes.

## Current status

RESERVE is a prototype. Its simulation results must be distinguished from real-world operational measurements. No emissions savings or commercial impact should be considered demonstrated without appropriate validation.

## Project contents

The repository will contain the application, simulation and evaluation code, tests, documentation, and demonstration materials as they are verified and added.


## Emissions comparison and evidence limits

The demo compares RESERVE's recommendation with the **nearest eligible processor**, applying the same shipment constraints to both. The nearest processor overall is shown separately because it may be infeasible. A modeled difference is not a measured reduction.

- The default factor of `0.1 kg CO₂e/(tonne-km)` is illustrative and unsourced; it is not an EPA factor.
- Candidate-specific factors can be supplied only with a source label. Record the source URL, data year, freight category, original units and any conversion before using a factor for real decisions.
- See [the emissions method and EPA reference notes](docs/EMISSIONS_METHOD.md). EPA SmartWay provides a relevant methodology and freight-carrier performance data, but does not validate the fictional processor profiles in this demo.
- With the same fallback factor for every candidate, the emissions ranking is equivalent to ranking by distance. The fair nearest-eligible baseline should therefore show **0% modeled improvement** unless defensible candidate-specific factors are supplied.
- No operational emissions reduction or real-world climate benefit is currently verified.

## Reproducibility and limitations

We aim to document data provenance, assumptions, calculation methods, test results, and known limitations. Estimates depend on the quality of the input data and the suitability of the emission factors used.

## Competition

Prepared for consideration in the IEEE ClimateChain Global Hackathon 2026. Final competition eligibility and submission requirements should be checked against the official rules.

## License

A license has not yet been selected.
