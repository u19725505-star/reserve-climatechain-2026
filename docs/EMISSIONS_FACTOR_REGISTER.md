# RESERVE emissions-factor register

**Register status:** Demonstration-only; no production-approved factor is currently registered.

| Factor ID | Value | Unit | Application | Source / evidence | Data year | Status | Allowed use |
|---|---:|---|---|---|---|---|---|
| DEMO-FALLBACK-001 | 0.1 | kg CO2e / metric tonne-km | Fallback in fictional demo | No source; deliberately illustrative | N/A | UNSOURCED — NOT VALIDATED | Demo behavior only; must not support real operational or climate-impact claims |

## Approval requirements for any new factor

Do not add a factor for real routing until the following fields are completed and reviewed:

- Unique factor ID and version.
- Numerical value and canonical units (kg CO2e / metric tonne-km for the current model).
- Publisher, exact source URL/document, publication date and data year.
- Freight mode, carrier/category, geography, and activity boundary.
- Whether the factor covers CO2 or CO2e, included gases, and GWP basis where relevant.
- Original reported units and reproducible conversion into canonical units.
- Whether measured, carrier-reported, modeled, category average, or proxy.
- Applicability rationale and known exclusions (e.g. empty returns, load factor, upstream fuel emissions).
- Reviewer, review date, and approval status.
- Sensitivity range or uncertainty description where available.

A source label by itself is not sufficient provenance. The code should not imply that a factor is facility-specific merely because it is attached to a processor profile. Preserve the source category and scope.

## Candidate sources to evaluate, not pre-approved factors

- U.S. EPA SmartWay shipper tools and technical documentation: https://www.epa.gov/smartway
- U.S. EPA SmartWay Sustainability Accounting and Reporting: https://www.epa.gov/smartway/smartway-sustainability-accounting-and-reporting
- U.S. EPA SmartWay High Performer Lists: https://www.epa.gov/smartway/smartway-high-performer-lists

These references are starting points for method and freight-category data. They do not establish a factor for a fictional RESERVE processor, and no number should be copied without checking current source version, category definitions, scope and units.
