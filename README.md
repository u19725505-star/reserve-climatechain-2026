# RESERVE — ClimateChain 2026

**Evidence-ready routing for circular materials**

[**Open the live demo**](https://reserve-climatechain.onrender.com/) · [Source code](https://github.com/u19725505-star/reserve-climatechain-2026) 

[![Python tests](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/tests.yml/badge.svg)](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/tests.yml)
[![Solidity tests](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/contract-tests.yml/badge.svg)](https://github.com/u19725505-star/reserve-climatechain-2026/actions/workflows/contract-tests.yml)

**Recommended hackathon track:** Sustainable Supply Chains.

RESERVE is a working web prototype that screens candidate material processors against shipment constraints, explains exclusions, compares eligible routing options, and records decision-support events in a locally verifiable audit chain.

> **Evidence boundary:** Demo processor profiles are fictional. The fallback transport factor is illustrative and unsourced. The weighted model is deterministic advisory decision support, not a trained machine-learning model. The local hash chain is not a decentralized blockchain. No real-world emissions reduction is claimed.

## Run locally

Python 3.11+ is recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open the local URL printed by Flask. Run the Python regression suite with:

```bash
python -m unittest discover -s tests -v
node --check static/app.js
```

For the Solidity prototype, install [Foundry](https://book.getfoundry.sh/) and run `forge test -vvv` from the repository root. A passing local contract test does not establish a public-chain deployment.

## Judge / reviewer quick links

- [Competition submission text and 3–5 minute demo script](docs/COMPETITION_SUBMISSION_PACK.md)
- [Explainable scoring and audit-chain design](docs/EXPLAINABLE_AI_AND_AUDIT_CHAIN.md)
- [Emissions calculation method](docs/EMISSIONS_METHOD.md)
- [Emissions-factor provenance register](docs/EMISSIONS_FACTOR_REGISTER.md)
- [Pilot data dictionary](docs/PILOT_DATA_DICTIONARY.md)
- [Proposed pilot evaluation protocol](docs/PILOT_EVALUATION_PROTOCOL.md)
- [Testnet deployment instructions and limitations](docs/TESTNET_DEPLOYMENT.md)

## The problem

A suitable processor may not be available when a shipment arrives. Material-quality uncertainty, capacity constraints, scheduling changes, and transport requirements can make routing decisions difficult to coordinate and audit.

## Implemented in this prototype

- **Eligibility-first screening:** checks material acceptance, available capacity, quality threshold, and delivery window before ranking.
- **Fair baseline:** compares the selected candidate with the nearest processor that satisfies the same shipment constraints.
- **Explainable decision support:** exposes deterministic criteria weights and per-candidate contributions; advisory only, not trained ML.
- **Local audit verification:** records decision-support events in a SHA-256 hash chain and verifies event hashes and previous-record links.
- **Smart-contract artifact:** includes a Solidity decision-registry prototype and automated Foundry tests; no public/testnet deployment has been verified.
- **Evidence documentation:** includes an emissions-factor register, calculation method, pilot data dictionary, and proposed shadow-mode evaluation protocol.

Conditional booking, live disruption reallocation, production processor integrations, and live on-chain transactions are not represented as completed capabilities.

## Current status

RESERVE is a prototype. Its simulation results must be distinguished from real-world operational measurements. No emissions savings or commercial impact should be considered demonstrated without appropriate validation.

## Project contents

The repository contains the Flask demonstration app, evaluation and ranking modules, automated tests, method documentation, and reproducible demo output. The demo profiles and fallback factor are synthetic/illustrative.

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

## Explainable decision support and audit-chain prototype

RESERVE now includes a deterministic explainable multi-criteria decision model exposed at `POST /api/decision-support`. It first enforces hard processor eligibility, then shows visible weighted criteria for modeled transport emissions (45%), quality margin (20%), capacity headroom (20%), and delivery-window fit (15%). These are illustrative decision-support weights, not a trained or validated machine-learning model. The result is advisory only.

Each decision-support request is recorded in a local SHA-256 hash-chained JSONL audit log. `GET /api/audit` and `POST /api/audit/verify` report whether the chain links and event hashes verify. This is a tamper-evident audit primitive, **not a decentralized blockchain**: it does not implement consensus, independent validators, or replicated storage. Do not claim a deployed blockchain until those components exist and are independently checked.

See [Explainable AI and audit-chain design](docs/EXPLAINABLE_AI_AND_AUDIT_CHAIN.md) for the model, weights, endpoints, threat boundaries, and limitations. The demo profiles remain fictional and the emissions factor remains illustrative and unsourced. No real climate benefit is demonstrated.


## Smart-contract registry prototype

The repository now includes [ReserveDecisionRegistry.sol](contracts/ReserveDecisionRegistry.sol), a Solidity registry that stores decision-record hashes, previous-hash links, model-version hashes, timestamps, and submitter addresses. Foundry tests and a separate GitHub Actions workflow are included. This is a deployable contract source, but **it has not yet been deployed to a public or test blockchain and the live web app does not yet submit transactions to it**. Until deployment, transaction integration, and network verification are completed, describe RESERVE as having a smart-contract registry prototype plus a local hash-chained audit log—not as a live decentralized blockchain system.

See [EXPLAINABLE_AI_AND_AUDIT_CHAIN.md](docs/EXPLAINABLE_AI_AND_AUDIT_CHAIN.md) for architecture and limitations.

## Testnet integration

The web interface includes an optional browser-wallet action to anchor a digest of the verified local audit chain to a configured deployment of the Solidity registry. It is disabled until a contract address is configured. Deployment and activation instructions are in [TESTNET_DEPLOYMENT.md](docs/TESTNET_DEPLOYMENT.md). The contract is not deployed by this repository automatically; a testnet deployment and independently confirmed transaction are required before claiming live on-chain integration.

## License

A license has not yet been selected.


## Blockchain demonstration mode

The website includes an explicitly labelled local demonstration identity and in-memory SHA-256 linked-record workflow. It does not create a real wallet, private key, signed transaction, or public-chain transaction. The demo is intended to make the evidence-anchoring sequence understandable without requiring personal information or cryptocurrency; its records exist only for the current browser page session.

The Solidity `ReserveDecisionRegistry` is a separate smart-contract prototype. The repository's automated Solidity workflow is the place to verify contract behavior in a local EVM. A successful local test is not the same as a deployed public-chain contract, and RESERVE must not claim public-chain anchoring until a deployment and transaction are independently verified.
