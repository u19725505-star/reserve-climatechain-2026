# RESERVE controlled pilot evaluation protocol

**Status:** Proposed protocol — not yet executed  
**Purpose:** Define the minimum evidence needed to test whether RESERVE improves material-routing decisions and whether any transport-emissions difference is real and defensible.

## 1. Research question

For eligible material shipments, does RESERVE's eligibility-constrained recommendation improve operational decision quality versus the organization's existing dispatch process, without worsening acceptance, service, cost, or other agreed constraints? Separately, does a properly bounded, activity-based transport calculation show a difference from a pre-specified fair baseline?

These are two separate questions. A routing recommendation can be operationally useful without demonstrating an emissions reduction.

## 2. Current evidence boundary

The public demo uses fictional processor profiles and an illustrative fallback factor of 0.1 kg CO2e per metric tonne-kilometre. It has not been validated against real shipments, processor records, carrier activity data, or measured emissions. Demo calculations are screening estimates, not a product/facility footprint or verified climate outcome.

Do not describe the current demo as proving emissions avoided, carbon savings, diversion outcomes, cost savings, or improved recovery rates.

## 3. Pre-registration before pilot

Before reviewing pilot outcomes, record:
- Pilot owner, participating sites/processors, dates, material categories, and operational scope.
- Eligibility definitions: accepted material/specification, capacity available at decision time, minimum quality, and delivery/processing window.
- Primary operational outcome and secondary outcomes.
- Baseline dispatch policy and comparison unit.
- Emissions boundary, activity data, factor source/version, unit conversions, and treatment of empty returns/return legs, load factors, and subcontracting.
- Exclusion rules, missing-data handling, analysis plan, and stop/escalation criteria.
- Data access, retention, privacy, and commercial-confidentiality arrangements.

Keep a dated copy of this protocol before the first analyzed shipment. Record deviations rather than silently changing the method.

## 4. Minimum shipment-level data

For each decision, collect a pseudonymous shipment ID; timestamp; material/specification; mass and unit; origin; requested delivery window; required quality; processors considered; each processor's acceptance status, capacity available at decision time, quality capability and availability evidence; rejection reason; proposed and actual destination; dispatch decision-maker; actual distance/route or vehicle activity; delivery/acceptance result; processing outcome; and exceptions/cancellations.

For emissions, prefer actual vehicle/fuel/energy activity and a method matched to the selected boundary. If using factors, preserve source URL or document, publisher, version/data year, freight mode/category, geography, pollutant scope, units, conversion, and whether measured, reported, modeled, or averaged. A source label alone is not enough for a production-grade factor.

## 5. Comparison design

Use the same shipment requirements for both methods.

**Operational baseline:** the documented existing dispatch process, captured before the RESERVE recommendation is revealed where feasible. Do not retrospectively redefine the baseline to make RESERVE look better.

**Algorithmic audit baseline:** nearest eligible processor under the same constraints. This is useful for checking ranking logic but is not a substitute for the existing-process baseline in a real-world impact study.

Run RESERVE in shadow mode first: generate recommendations without controlling dispatch. Compare recommendation feasibility with the actual decision and outcome. Only consider a controlled rollout after data quality, safety, and operational review. If randomization or matched comparison is feasible, define the assignment and analysis before the pilot; otherwise state the confounding limits of a before/after or observational design.

## 6. Outcomes and analysis

Pre-specify one primary operational outcome, such as the proportion of shipments assigned to a destination that accepts the shipment and meets required constraints. Possible secondary outcomes include rejection/re-routing rate, on-time arrival, processing completion, distance, total transport cost, time to assign, and completeness of decision records.

Report denominator, missingness, uncertainty, and results by material/site where sample size permits. Do not count a recommendation as a successful outcome until its actual feasibility and result are observed.

For transport emissions, calculate both baseline and RESERVE cases using a consistent boundary and defensible factors. Report activity data and factor provenance alongside estimates. Include sensitivity analysis for material assumptions and factor ranges. Do not infer whole-system climate benefit from distance alone; account for any changed processing route, mode, load, return legs, and other material boundary differences where relevant.

## 7. Quality gates

Do not publish a climate-impact claim unless:
1. Actual operational records have been reconciled to source records.
2. Baseline and intervention boundaries are comparable and documented.
3. Factors are appropriate to the activity, sourced, versioned, and unit-checked.
4. Exclusions, missing records, and uncertainty are disclosed.
5. The calculation can be independently reproduced.
6. A qualified reviewer has reviewed the method and evidence.

A pilot that finds no reduction, or an increase, must be reported honestly. Null or adverse findings are valid evidence.

## 8. Suggested acceptance gates (to be agreed before pilot)

These are proposed governance gates, not achieved results:
- 100% of recommendations include machine-readable eligibility results and exclusion reasons.
- 100% of analyzed shipments have traceable source records for the variables used in the decision.
- No infeasible recommendation is counted as an operational success.
- Every reported emissions estimate has a documented boundary, factor/activity provenance, units, and reproducible calculation.
- No public quantitative impact claim before data-quality and independent-review gates are passed.

Set minimum sample size and performance thresholds with the pilot owner after inspecting expected shipment volumes and variability; do not invent statistical power or claim generalizability from a small convenience sample.

## 9. Deliverables

Publish a versioned, reproducible evidence bundle containing this protocol and amendments; a data dictionary; anonymized analysis dataset where permitted; factor register; test results; analysis script/version; aggregate tables and uncertainty/sensitivity analysis; deviations and missingness log; reviewer sign-off; and a limitations statement. Protect commercially sensitive and personally identifiable data.

## 10. Current conclusion

RESERVE is a working decision-support prototype with a transparent fictional demo. Operational usefulness and environmental impact remain hypotheses to test. The next credible milestone is a shadow-mode pilot with real, traceable shipment and processor data—not a larger modeled savings claim.
