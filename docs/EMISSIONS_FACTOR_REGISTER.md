# Emissions-Factor Register

## Status
This register documents the factor provenance currently known for the RESERVE proof of concept. It intentionally distinguishes an illustrative fallback from a sourced factor.

| Factor / input | Current value or status | Provenance | Permitted interpretation |
|---|---|---|---|
| Fallback transport factor | `0.1 kg CO₂e/(tonne-km)` | Illustrative; no authoritative source recorded | Demonstration only; not a verified factor |
| Processor profiles | Fictional | Synthetic demo data | Do not infer real facility operations |
| Route distance | Used by the estimator | Demo route/input data | Not proof of an actual shipment route |
| Candidate-specific factors | Not established as validated real-world data | Requires future data sourcing | Do not claim comparative climate advantage from unverified values |

## Sourcing checklist
Before adding a production factor, record:
- unique factor ID and version;
- publisher, dataset title, URL or DOI, and retrieval date;
- publication/data year;
- geographic and freight-category applicability;
- original units and conversions;
- well-to-wheel or tank-to-wheel boundary, as applicable;
- load factor, vehicle class, fuel, and empty-running assumptions;
- uncertainty and limitations;
- reviewer and approval date.

## Governance rule
Do not silently replace or relabel the fallback as an official factor. Any new factor should be versioned, source-traceable, and accompanied by an explanation of how it changes estimates and the nearest-eligible comparison.

See [Emissions Method](EMISSIONS_METHOD.md) for the calculation and interpretation rules.
