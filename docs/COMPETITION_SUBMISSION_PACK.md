# RESERVE ClimateChain 2026 — Competition Submission Pack

## Project summary
RESERVE is a proof-of-concept decision-support workflow for circular-material routing. It screens candidate processors against shipment constraints, explains a deterministic ranking, estimates transport emissions using explicit assumptions, and records decision evidence in a local hash-chained audit log.

## Problem
The nearest facility is not necessarily suitable: it may not accept a material, have sufficient capacity, meet quality requirements, or fit the delivery window. Routing recommendations should expose these constraints and the reasoning behind a choice.

## What to demonstrate
1. Open the [live app](https://reserve-climatechain.onrender.com/).
2. Enter a synthetic shipment: material, quantity, quality requirement, and delivery window.
3. Review which fictional processors pass or fail eligibility checks and why.
4. Compare eligible candidates and inspect the deterministic score contributions.
5. Review the transport-emissions estimate, factor, units, and nearest-eligible baseline.
6. Inspect audit-chain verification.
7. Treat the Solidity registry as a separate contract prototype; do not imply it is deployed or connected to live transactions.

For a guided route, use the [judge walkthrough](https://reserve-climatechain.onrender.com/judges). The [demo video](https://www.youtube.com/watch?v=DFO8bHf4XKA) provides an overview.

## Current implementation
- Python/Flask backend and HTML/CSS/JavaScript frontend.
- Eligibility-first rules and deterministic multi-criteria ranking.
- Illustrative transport-emissions calculations.
- Local SHA-256 hash-chained JSONL audit log and verification endpoints.
- Separate Solidity registry prototype with Foundry tests.
- GitHub Actions workflows for Python and Solidity tests.

## Evidence and limitations
- Processor profiles are fictional; operational acceptance, capacity, and delivery data are not integrated.
- The fallback factor of `0.1 kg CO₂e/(tonne-km)` is illustrative and unsourced.
- The ranking is deterministic decision support, not trained machine learning.
- When all candidates use the same factor, emissions ranking is equivalent to distance ranking; comparison against the nearest eligible processor should show 0% modeled improvement unless defensible candidate-specific factors are used.
- The local audit chain is not a decentralized blockchain.
- Public/testnet contract deployment and live on-chain transactions have not been verified.
- No measured or independently verified climate savings are claimed.

## Recommended reviewer links
- [Live app](https://reserve-climatechain.onrender.com/)
- [Judge walkthrough](https://reserve-climatechain.onrender.com/judges)
- [Source repository](https://github.com/u19725505-star/reserve-climatechain-2026)
- [Demo video](https://www.youtube.com/watch?v=DFO8bHf4XKA)

## Proposed next steps
Validate with real, permissioned processor and shipment data; replace illustrative factors with traceable sources; test against an equivalent baseline; run in shadow mode; and evaluate results independently before any operational use.
