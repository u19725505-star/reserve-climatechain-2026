# RESERVE pilot data dictionary

**Status:** Proposed schema for shadow-mode pilot data; no operational dataset is currently attached to the public demo.

Use one row per shipment-decision event unless a field explicitly belongs to a separate processor or activity table. Prefer pseudonymous identifiers. Preserve source-system IDs only in a controlled crosswalk outside the analysis dataset.

| Field | Type / unit | Required | Definition / validation |
|---|---|---|---|
| shipment_id | string | Yes | Pseudonymous stable identifier; no direct personal identifiers |
| decision_timestamp | ISO 8601 with timezone | Yes | When dispatch decision was made |
| material_category | controlled string | Yes | Material class/specification used for eligibility |
| shipment_mass_tonnes | positive number, metric tonnes | Yes | Reconciled shipment mass; preserve original source unit separately |
| origin_id | pseudonymous string | Yes | Origin site identifier; coordinates/address held in controlled operational system |
| required_quality | numeric 0–1 or documented native scale | Yes | Define scale and meaning before analysis; do not mix scales |
| earliest_delivery / latest_delivery | timestamp/date | Yes | Acceptable delivery window; latest must not precede earliest |
| processor_id | string | Yes per candidate | Stable processor identifier |
| candidate_accepts_material | boolean + source reference | Yes per candidate | Acceptance evidence valid at decision time |
| available_capacity_tonnes | non-negative number | Yes per candidate | Capacity available at decision time, not nominal capacity unless explicitly stated |
| processor_quality_capability | numeric/documented scale | Yes per candidate | Evidence and measurement date required |
| available_from / available_until | timestamp/date | Yes per candidate | Availability evidence as known at decision time |
| route_distance_km | non-negative number | Yes if distance model used | Route source, route type, date and calculation method required |
| eligibility_result | boolean | Yes per candidate | Computed from versioned rules; do not manually overwrite |
| exclusion_reasons | list of controlled codes | Yes per candidate | Machine-readable reasons plus human-readable explanation |
| reserve_rank | positive integer or null | Yes per candidate | Null for ineligible candidates; ranker version recorded |
| reserve_recommendation | processor ID or null | Yes per shipment | Null if no candidate is eligible |
| actual_destination_id | string or null | Yes after dispatch | Actual destination from operational record |
| actual_acceptance_result | boolean/unknown | Yes after processing | Evidence source and observation timestamp required |
| actual_delivery_time | timestamp or null | Recommended | Actual event record; distinguish missing from not applicable |
| reroute_or_rejection | controlled code or null | Recommended | Reason and source record required |
| transport_activity | structured value + unit | Required for activity-based emissions | Fuel, vehicle-km, tonne-km, mode, load, and return-leg information appropriate to chosen method |
| emissions_factor_id | string | Required if factor-based | Foreign key into versioned factor register |
| emissions_estimate_kg_co2e | non-negative number or null | Required if calculated | Reproducible output; include method/version and boundary |
| existing_process_decision | processor ID or null | Yes for comparison | Baseline decision recorded before recommendation is revealed where feasible |
| missing_data_flags | list | Yes | Explicitly identifies absent, estimated, imputed or conflicting fields |
| source_record_refs | list of controlled references | Yes | Auditable provenance without embedding sensitive records in public outputs |

## Data handling rules

- Keep raw records, analysis-ready data, and any identity crosswalk separate.
- Record units, source, timestamp, and data transformations for every derived field.
- Distinguish zero from missing, unavailable, not applicable, and not measured.
- Snapshot candidate capacity and availability as known at decision time; current values cannot be substituted retrospectively.
- Version eligibility rules, ranker, factor register, and analysis code.
- Do not publish commercially sensitive route, processor, or shipment details without permission.
