# Pilot Data Dictionary

## Purpose
This is a proposed data dictionary for a future permissioned shadow-mode pilot. These fields are not evidence that live processor or shipment integrations currently exist.

| Entity | Field | Meaning | Example / notes |
|---|---|---|---|
| Shipment | `shipment_id` | Pseudonymous unique shipment identifier | Avoid personal data |
| Shipment | `material_type` | Declared recovered-material category | Controlled vocabulary |
| Shipment | `mass_tonnes` | Shipment mass in metric tonnes | Positive numeric value |
| Shipment | `quality_requirement` | Minimum required material quality | Define scale and validation |
| Shipment | `delivery_window_start` | Earliest acceptable delivery | Timestamp with timezone |
| Shipment | `delivery_window_end` | Latest acceptable delivery | Timestamp with timezone |
| Processor | `processor_id` | Stable facility identifier | Access-controlled mapping |
| Processor | `accepted_materials` | Materials the facility accepts | Confirm with facility |
| Processor | `available_capacity_tonnes` | Capacity available for the relevant period | Include observation timestamp |
| Processor | `quality_capability` | Supported quality range | Document measurement method |
| Processor | `delivery_constraints` | Operational receiving window | Keep current and auditable |
| Route | `distance_km` | Estimated or observed route distance | Label source and method |
| Emissions | `factor_id` | Versioned emissions-factor reference | Must resolve to source register |
| Emissions | `factor_value` | Factor value and units | Never store a unitless factor |
| Decision | `model_version` | Version of rules and weights | Include configuration hash |
| Decision | `eligible` | Whether hard constraints pass | Include exclusion reasons |
| Decision | `score_components` | Criterion-level score contributions | Preserve units and weight version |
| Audit | `event_hash` | Hash of canonicalized event | Specify canonical serialization |
| Audit | `previous_hash` | Previous event hash | Genesis convention must be documented |
| Outcome | `delivery_status` | Observed delivery result | Collect only when available |
| Outcome | `actual_mass_tonnes` | Actual shipped mass | Compare with planned mass |
| Outcome | `actual_transport_data` | Data needed for a measured estimate | Record source and quality |

## Data-quality requirements
- Define units, valid ranges, null handling, and timestamp/timezone conventions.
- Record provenance and observation time for mutable capacity and acceptance data.
- Use pseudonymous IDs and minimize personal or commercially sensitive information.
- Preserve both the recommendation-time snapshot and later observed outcomes.
- Keep synthetic demonstration data clearly labeled as synthetic.

See [Pilot Evaluation Protocol](PILOT_EVALUATION_PROTOCOL.md) for proposed collection and evaluation.
