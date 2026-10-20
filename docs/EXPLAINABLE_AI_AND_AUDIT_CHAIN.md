# Explainable Decision Support and Audit-Chain Design

## Scope
RESERVE currently uses deterministic eligibility rules and configurable scoring weights. It is not a trained machine-learning system. This document describes the prototype's decision and audit boundaries.

## Eligibility before ranking
A candidate must satisfy the shipment's configured requirements before it can be ranked. Checks include:
- material acceptance;
- available capacity;
- required quality;
- delivery-window fit.

Excluded candidates should be accompanied by human-readable reasons. The recommendation is advisory, not an automated dispatch command.

## Ranking criteria
The current illustrative weights are:

| Criterion | Weight |
|---|---:|
| Estimated transport emissions | 45% |
| Quality margin | 20% |
| Capacity headroom | 20% |
| Delivery-window fit | 15% |

These are configurable decision parameters, not learned coefficients. They have not been validated against real operational outcomes. A score is only meaningful relative to the inputs, constraints, and assumptions used for that run.

## Climate estimate
The prototype estimates transport emissions from shipment quantity, route distance, and a configured or fallback factor. The fallback value is illustrative and unsourced. See [Emissions Method](EMISSIONS_METHOD.md) and [Emissions-Factor Register](EMISSIONS_FACTOR_REGISTER.md).

## Local audit chain
The application records decision-support events in a local JSONL log with SHA-256 hash links. Verification can detect modifications that break the stored chain. A hash chain alone does not provide independent consensus, replicated storage, an external timestamp authority, or decentralized-blockchain guarantees.

Relevant endpoints documented by the project:
- `POST /api/decision-support` — evaluate candidates and record a decision-support event.
- `GET /api/audit` — inspect audit-chain verification status.
- `POST /api/audit/verify` — explicitly verify the chain without mutating it.
- `GET /health` — inspect service/configuration status.

## Threat boundaries
The chain is a tamper-evidence mechanism, not proof that submitted inputs are true. An actor with sufficient access to rewrite the entire log and recompute every hash may defeat checks that rely only on that same log. Stronger assurances would require protected checkpoints, independent storage, access controls, and a documented retention policy.

## Solidity prototype
The repository contains a separate Solidity registry prototype and Foundry tests. The local audit log and contract are not represented as integrated. A passing contract test is not evidence of deployment. See [Testnet Deployment Notes](TESTNET_DEPLOYMENT.md).

## Safe interpretation
Use the output to inspect and compare options. Do not use this prototype as a production dispatch system, assume its synthetic records represent real facilities, or treat estimates as verified environmental outcomes.
