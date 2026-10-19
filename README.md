# RESERVE — Climate-Aware Routing for Circular Materials

**Evidence-ready routing for circular materials.**  
RESERVE screens processors for operational eligibility, explains its recommendations, estimates transport emissions, and records decision evidence.

<p align="center">
  <a href="https://reserve-climatechain.onrender.com/"><strong>Open the live demo</strong></a> ·
  <a href="https://reserve-climatechain.onrender.com/judges"><strong>Follow the judge walkthrough</strong></a> ·
  <a href="https://youtu.be/DFO8bHf4XKA"><strong>Watch the demo video</strong></a> ·
  <a href="https://devpost.com/software/reserve-climate-aware-resource-routing"><strong>Devpost project</strong></a>
</p>

[![Python tests](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/tests.yml/badge.svg)](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/tests.yml)
[![Solidity tests](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/contract-tests.yml/badge.svg)](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/contract-tests.yml)

**Competition context:** IEEE ClimateChain Global Hackathon 2026  
**Proposed track alignment:** Sustainable Supply Chains

> **Evidence and scope:** This is a publicly accessible proof-of-concept application. Processor profiles are fictional, and the default transport-emissions factor is illustrative and unsourced. The scoring model is deterministic decision support—not trained machine learning. The local audit log is not a decentralized blockchain. The Solidity registry is a separate prototype; public/testnet deployment and live on-chain transactions have not been verified. No measured or independently verified climate savings are claimed.

---

## Start here: judge walkthrough

The fastest way to evaluate RESERVE is to open the [guided six-step walkthrough](https://reserve-climatechain.onrender.com/judges), then try the [live application](https://reserve-climatechain.onrender.com/). No local installation, wallet, cryptocurrency, or personal information is required for the demonstration.

### Six steps to evaluate the project

1. **Understand the problem.** Circular-material routing is not simply a nearest-destination problem: a processor must be able to accept and handle the shipment.
2. **Enter shipment requirements.** Set material type, quantity, required quality, and delivery window.
3. **Inspect eligibility.** See which fictional processors pass or fail hard constraints and read the reasons for exclusions.
4. **Review the recommendation.** Compare eligible candidates and inspect the deterministic multi-criteria scoring explanation.
5. **Challenge the climate estimate.** Review the transport-emissions assumptions and compare the selected option with the nearest eligible processor under the same shipment constraints.
6. **Verify the evidence boundary.** Inspect the local hash-chained audit verification and the separate Solidity registry prototype; note what is implemented and what remains future work.

The walkthrough is designed to help reviewers understand the problem, the workflow, the decision logic, the climate assumptions, and the project's current limits without needing to infer them from the source code.

## Demo video

[**Watch the RESERVE demonstration on YouTube**](https://youtu.be/DFO8bHf4XKA)

The video accompanies the live prototype and repository. For the most complete review, watch the video and then reproduce the workflow in the [live app](https://reserve-climatechain.onrender.com/).

## The problem

Recovered materials need destinations that can accept the material, meet quality requirements, accommodate shipment volume, and satisfy delivery constraints. A geographically close facility may be infeasible. A ranking that hides exclusion reasons or climate assumptions can also be difficult to scrutinize.

RESERVE explores an eligibility-first, explainable decision-support workflow for circular-material logistics. It is intended as a starting point for evidence-led evaluation—not a production dispatch system.

## What the prototype does

- **Eligibility-first screening:** checks material acceptance, available capacity, required quality, and delivery window before ranking candidates.
- **Explainable ranking:** ranks eligible options using visible criteria and per-candidate contributions.
- **Nearest-eligible baseline:** compares the selected candidate with the nearest processor that satisfies the same shipment constraints. The nearest processor overall is shown separately because it may be ineligible.
- **Illustrative emissions estimates:** calculates screening estimates from shipment quantity, route distance, and a configured or fallback emissions factor.
- **Tamper-evident local audit log:** records decision-support events in a SHA-256 hash chain and provides endpoints to inspect and verify the chain.
- **Solidity registry prototype:** includes a smart-contract artifact and Foundry tests for hash-linked decision evidence.
- **Reproducible engineering trail:** includes Python tests, contract tests, CI workflows, and documentation for emissions assumptions and a future pilot evaluation.

### Explainable decision-support model

The current deterministic model applies illustrative weights to four criteria:

| Criterion | Weight |
|---|---:|
| Estimated transport emissions | 45% |
| Quality margin | 20% |
| Capacity headroom | 20% |
| Delivery-window fit | 15% |

Eligibility is enforced before ranking. The weights are configurable decision parameters, not learned coefficients, and the model has not been validated against real operational outcomes. Its recommendation is advisory only.

## Climate methodology: what the numbers mean

The demo's emissions figures are **illustrative estimates**, not measurements. They are intended to expose the calculation and make assumptions inspectable.

- The default fallback factor is `0.1 kg CO₂e/(tonne-km)`; it is illustrative and unsourced, not an EPA factor.
- Processor profiles are fictional. The demo does not establish real facility capacity, material acceptance, transport activity, or actual emissions.
- The comparison baseline is the **nearest eligible processor** under the same shipment constraints. The nearest processor overall is shown separately and may be excluded.
- When the same fallback factor is used for every candidate, emissions ranking is equivalent to distance ranking. The nearest-eligible baseline should therefore show **0% modeled improvement** unless defensible candidate-specific factors change the comparison.
- A modeled difference is not a measured or verified reduction. No real-world climate benefit is established by this prototype.

Before a real pilot, each factor should have a traceable source, publication/data year, freight category, original units, conversion method, system boundary, and uncertainty notes. See [Emissions Method](docs/EMISSIONS_METHOD.md) and [Emissions-Factor Register](docs/EMISSIONS_FACTOR_REGISTER.md).

## Auditability and blockchain scope

### Local audit chain

Decision-support events are recorded in a local SHA-256 hash-chained JSONL log. The application exposes:

- `POST /api/decision-support` — evaluate eligible candidates and record a decision-support event.
- `GET /api/audit` — inspect audit-chain verification status.
- `POST /api/audit/verify` — explicitly verify the chain without mutating it.
- `GET /health` — inspect service and configuration status.

A hash chain can help reveal changes to recorded events when verified against the chain. By itself, it does not provide consensus, independent validators, replicated storage, or the guarantees of a decentralized blockchain.

### Solidity registry prototype

The repository includes [`contracts/ReserveDecisionRegistry.sol`](contracts/ReserveDecisionRegistry.sol), with Foundry tests in `test-contracts/` and a separate GitHub Actions workflow. The contract is designed to anchor decision-record hashes, previous-hash links, model-version hashes, timestamps, and submitter addresses.

**Deployment status:** A public/testnet deployment and live on-chain transaction integration have not been independently verified. The local audit log and the Solidity contract are separate components. Do not interpret a passing local contract test as evidence of a deployed blockchain.

See [Testnet Deployment Notes](docs/TESTNET_DEPLOYMENT.md) for the deployment path and requirements.

## Architecture and technology

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript
- **Decision logic:** eligibility rules and deterministic multi-criteria scoring
- **Audit:** SHA-256 hash-chained local event log
- **Smart-contract prototype:** Solidity, Foundry
- **Hosting:** Render
- **Automation:** GitHub Actions for Python and Solidity test workflows

The system is not currently a trained machine-learning application. It does not perform live processor integrations, production dispatch, or verified on-chain writes.

## Run locally

Python 3.11 or newer is recommended.

```bash
git clone https://github.com/u19725505-star/reserve-climatechain-2026.git
cd reserve-climatechain-2026

python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows PowerShell
# .venv\Scripts\Activate.ps1

python -m pip install -r requirements.txt
python app.py
```

Open the local address printed by Flask (normally `http://127.0.0.1:5000`).

### Run checks

Run the Python regression tests and JavaScript syntax check:

```bash
python -m unittest discover -s tests -v
node --check static/app.js
```

To test the Solidity registry, install [Foundry](https://book.getfoundry.sh/) and run:

```bash
forge test -vvv
```

The GitHub Actions workflows provide an additional automated test record:

- [Python test workflow](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/tests.yml)
- [Solidity contract-test workflow](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/contract-tests.yml)

A successful test run supports the tested code paths; it does not establish real-world climate performance or public-chain deployment.

## Reviewer documentation

| Document | What it covers |
|---|---|
| [Competition submission pack](docs/COMPETITION_SUBMISSION_PACK.md) | Submission narrative and demo guidance |
| [Explainable AI and audit-chain design](docs/EXPLAINABLE_AI_AND_AUDIT_CHAIN.md) | Scoring, weights, endpoints, threat boundaries, and limitations |
| [Emissions method](docs/EMISSIONS_METHOD.md) | Calculation method and reference notes |
| [Emissions-factor register](docs/EMISSIONS_FACTOR_REGISTER.md) | Factor provenance and data requirements |
| [Pilot data dictionary](docs/PILOT_DATA_DICTIONARY.md) | Proposed operational data fields |
| [Pilot evaluation protocol](docs/PILOT_EVALUATION_PROTOCOL.md) | Proposed shadow-mode evaluation |
| [Testnet deployment notes](docs/TESTNET_DEPLOYMENT.md) | Contract deployment requirements and limitations |

## Limitations and next milestones

RESERVE is not yet a validated operational routing service. Its present limitations include synthetic processor profiles, an illustrative fallback emissions factor, no demonstrated measured climate benefit, and no verified public-chain deployment or live transaction integration.

The next milestones are:

1. Obtain permission to evaluate realistic processor acceptance, capacity, shipment, and delivery data.
2. Replace the fallback factor with traceable, scenario-appropriate emissions factors and document uncertainty and boundaries.
3. Compare recommendations against a defensible baseline under equivalent constraints.
4. Run in shadow mode alongside existing operations without controlling dispatch.
5. Evaluate feasibility, rejection rates, delivery performance, and estimated emissions with independent review.
6. Deploy and verify the contract on a test network only if on-chain anchoring provides a clear benefit over the local audit trail.

## Competition context

This project was prepared for consideration in the **IEEE ClimateChain Global Hackathon 2026**. It is intended to align with sustainable supply-chain decision support by making material-routing constraints and climate-estimation assumptions more transparent. Please verify the official track options, eligibility, deadline, and submission status on the [official hackathon page](https://ieee-climatechain-hack.devpost.com/) and [rules](https://ieee-climatechain-hack.devpost.com/rules).

## License

A license has not yet been selected. Unless and until a license is added, do not assume the repository grants permissions beyond the rights provided by applicable law.

---

**Better routing decisions. Transparent evidence. Measurable climate impact—when validated.**
