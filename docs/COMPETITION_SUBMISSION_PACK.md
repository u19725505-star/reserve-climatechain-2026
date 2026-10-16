# RESERVE — ClimateChain 2026 submission pack

**Purpose:** A working draft for the IEEE ClimateChain Global Hackathon 2026 submission. Review against the live official rules before submitting.

## 1. Recommended track

**Sustainable Supply Chains**

RESERVE addresses a practical circular-materials coordination problem: a shipment should not be sent to a processor that cannot accept its material, lacks available capacity, fails quality requirements, or cannot meet the delivery window. It makes candidate screening and the reasons behind each decision visible, while keeping environmental estimates separate from verified outcomes.

This is a prototype contribution to sustainable-supply-chain decision support. It does not yet prove that routing changes reduce emissions.

## 2. Submission title

**RESERVE: Evidence-Ready Routing for Circular Materials**

## 3. Draft project description

Circular-material shipments can be delayed, rejected, or rerouted when processor acceptance rules, available capacity, quality requirements, and delivery windows are not checked together. When routing decisions are difficult to audit, it is also difficult to determine whether a proposed change genuinely improves operational performance or environmental outcomes.

RESERVE is a web-based prototype for sustainable circular-material routing. It screens processors against shipment constraints, explains exclusions, compares the selected option with a fair nearest-eligible baseline, and includes an explainable multi-criteria decision-support model. The model scores only eligible processors using visible weights for transport-emissions estimates, quality margin, capacity headroom, and delivery-window fit. It is deterministic advisory decision support—not a trained or operationally validated machine-learning model.

The project also includes a SHA-256 hash-chained audit log and a Solidity smart-contract registry prototype for anchoring decision hashes. The local audit API is integrated into the web app. The Solidity contract has been added to the repository with Foundry tests, but it has not yet been deployed to a public or test network and the web app does not yet submit on-chain transactions. The project is therefore **blockchain-oriented and smart-contract-ready, but not yet a live decentralized blockchain deployment**.

The current demo uses fictional processor profiles and an intentionally illustrative, unsourced transport-emissions factor. It demonstrates decision logic and evidence discipline—not measured savings. The project includes automated regression tests, an emissions-factor provenance register, a proposed pilot data dictionary, and a controlled shadow-mode evaluation protocol. These artifacts define how a future real deployment could record decisions, source factors, compare outcomes, and report uncertainty.

The next milestone is a shadow-mode pilot with real processor acceptance/capacity records, shipment outcomes, and traceable transport activity. Any future AI or ledger component should be introduced only with a clearly defined purpose, reproducible evaluation, and an honest statement of what is and is not decentralized or independently verified.

## 4. What is implemented versus not yet demonstrated

### Implemented in the current prototype

- Flask web interface and JSON evaluation endpoint.
- Eligibility screening for material, available capacity, quality, and delivery window.
- Ranking of eligible processors using the configured transport-emissions estimate.
- Separate nearest-overall and nearest-eligible baseline logic.
- Input validation and machine-readable exclusion reasons.
- Explainable weighted decision-support endpoint and browser interface (advisory only; not trained ML).
- Local SHA-256 hash-chained audit log with verification endpoint.
- Solidity decision-evidence registry source plus Foundry test configuration.
- Explicit disclosure of fictional demo data and illustrative emissions.
- Automated Python and Solidity test workflows on GitHub Actions.
- Emissions method notes, factor register, pilot data dictionary, and proposed evaluation protocol.

### Not yet implemented or demonstrated

- Real processor, shipment, carrier, route, or facility data.
- A sourced and approved factor for each real transport scenario.
- Measured emissions, cost savings, rejection reduction, or operational improvement.
- A live controlled pilot or independent review.
- A trained or operationally validated machine-learning model.
- A deployed smart contract, live network transaction integration, replicated ledger, or decentralized consensus. The Solidity registry is source code only until deployment and integration are verified.

Do not describe any item in the second list as a completed feature. If an AI or blockchain capability is added before submission, update this section only after the implementation and tests are verified.

## 5. Three-to-five-minute demo video script

**0:00–0:25 — Problem and track**  
“RESERVE is a sustainable-supply-chain prototype for circular materials. A processor recommendation is only useful if the destination can actually accept the material, has capacity, meets quality requirements, and can meet the delivery window.”

**0:25–1:15 — Run the default scenario**  
Open the live site. Use the default recycled-plastic shipment (7 tonnes, quality threshold 0.80, delivery days 5–8). Show which processors are eligible and which are excluded. Explain at least one exclusion: the nearest processor overall is not feasible for this quantity because its demo capacity is too small.

**1:15–2:00 — Explain the fair baseline**  
Show the recommended candidate and nearest eligible baseline. Explain that comparing against an ineligible nearest processor would be misleading. With the same illustrative factor applied across candidates, ranking is effectively distance-based and the default scenario does not establish an emissions improvement.

**2:00–2:45 — Change a constraint**  
Increase shipment quantity or change the material/delivery window. Show how eligibility changes and how the API returns reasons. If no candidate qualifies, show that the system reports no eligible option instead of inventing a feasible recommendation.

**2:45–3:35 — Evidence and trust**  
Briefly show the repository's factor register and pilot protocol. Explain the distinction between a modeled estimate and a verified climate outcome, and the records a pilot would need.

**3:35–4:10 — Honest limitations and next step**  
“The demo data are fictional and the fallback factor is unsourced. We have not measured emissions reductions. Our next milestone is a shadow-mode pilot with traceable operational data and a pre-specified comparison against the existing dispatch process.”

**4:10–4:30 — Close**  
“RESERVE is designed to make circular-material routing decisions more explicit and auditable, while making the evidence gap visible instead of hiding it.”

Record the actual UI and current behavior; do not narrate features that are not present in the deployed build. Aim for 4–4.5 minutes.

## 6. Suggested judge-facing summary

- **Climate challenge:** Sustainable materials can fail to reach suitable processors when operational constraints are fragmented.
- **Prototype contribution:** Eligibility-first routing, explainable exclusions, and fair-baseline comparison.
- **Technical evidence:** Flask API, modular evaluation/ranking logic, automated tests, and a passing GitHub Actions run.
- **Responsible climate claims:** Synthetic inputs and unsourced fallback factor are explicitly disclosed; no real savings are claimed.
- **Path to validation:** Shadow-mode pilot, traceable operational records, approved factor provenance, uncertainty analysis, and independent review.

## 7. Final submission checklist

- [ ] Confirm eligibility and registration requirements directly in the official event rules.
- [ ] Explicitly select **Sustainable Supply Chains** in the project description.
- [ ] Re-open the deployed website and confirm the default scenario and health endpoint.
- [ ] Keep the public repository link accessible and include setup/testing instructions.
- [ ] Confirm the latest GitHub Actions run is green immediately before submission.
- [ ] Record and publish a 3–5 minute demo video; test its public link in a signed-out browser.
- [ ] Include a short description of the target user, workflow, scalability/adoption path, and limitations.
- [ ] Do not claim measured emissions savings, AI performance, blockchain immutability, or pilot results without direct evidence.
- [ ] Check the event's current deadline and any conflicting timing statements on the official page before submitting. The current Devpost overview lists **October 25, 2026 at 5:00 p.m. UTC+3**; treat the event page/rules as authoritative and verify the exact submission window.
- [ ] Submit the project on Devpost itself; a public website and repository alone do not constitute a completed entry.

## 8. Project links

- Explainable AI and audit-chain architecture: [EXPLAINABLE_AI_AND_AUDIT_CHAIN.md](EXPLAINABLE_AI_AND_AUDIT_CHAIN.md)
- Solidity registry: [ReserveDecisionRegistry.sol](../contracts/ReserveDecisionRegistry.sol)
- Foundry contract tests: [ReserveDecisionRegistry.t.sol](../test-contracts/ReserveDecisionRegistry.t.sol)
- Python tests for scoring and audit verification: [test_ai_and_ledger.py](../tests/test_ai_and_ledger.py)

- Live demo: https://reserve-climatechain.onrender.com/
- Repository: https://github.com/u19725505-star/reserve-climatechain-2026
- Automated test run: https://github.com/u19725505-star/reserve-climatechain-2026/actions/runs/38982482075
- Pilot protocol: [PILOT_EVALUATION_PROTOCOL.md](PILOT_EVALUATION_PROTOCOL.md)
- Data dictionary: [PILOT_DATA_DICTIONARY.md](PILOT_DATA_DICTIONARY.md)
- Emissions factor register: [EMISSIONS_FACTOR_REGISTER.md](EMISSIONS_FACTOR_REGISTER.md)
- Emissions method: [EMISSIONS_METHOD.md](EMISSIONS_METHOD.md)
