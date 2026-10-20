# Pilot Evaluation Protocol

## Status and objective
This is a proposed evaluation plan, not a report of completed field testing. The goal is to determine whether eligibility-first, explainable routing support improves decision quality in a real operational context without controlling dispatch.

## Study design
1. Obtain written permission and define participating sites, materials, and time period.
2. Establish data governance, privacy, retention, and access controls.
3. Run RESERVE in shadow mode alongside existing human workflows; do not send dispatch instructions.
4. Freeze and version eligibility rules, score weights, emissions factors, and the baseline definition before analysis.
5. Log recommendations, exclusions, explanations, and data-quality issues.
6. Compare recommendations with a defensible baseline under equivalent shipment constraints.
7. Have operational and environmental reviewers assess results and limitations.

## Suggested measures
- **Feasibility:** fraction of recommended processors that meet confirmed operational constraints.
- **Exclusion quality:** correctness and completeness of exclusion reasons.
- **Decision time:** time to reach a reviewable recommendation, measured consistently.
- **Acceptance / rejection:** processor acceptance and reasons for rejection.
- **Delivery performance:** on-time delivery and constraint compliance.
- **Emissions estimate quality:** factor provenance, input coverage, uncertainty, and comparison with an approved method.
- **Human factors:** reviewer comprehension, trust calibration, and override frequency.

## Baseline and analysis
Use the nearest eligible processor under the same constraints as one baseline, and document other comparators before collecting outcomes. Report denominators, missing data, uncertainty, and subgroup results where sample sizes support them. Separate observed outcomes from model estimates. Do not claim causal effects without a design that supports causal inference.

## Safety and governance
- Human operators retain decision authority.
- The prototype does not control dispatch or equipment.
- Use only authorized data and minimize sensitive information.
- Record protocol changes and deviations.
- Define stop criteria for data-quality failures or operational risk.

## Reporting
Publish the versioned protocol, data dictionary, factor register, sample counts, exclusions, uncertainty, and negative results where possible. Do not claim climate savings unless measured using a defensible methodology and independently reviewed.
