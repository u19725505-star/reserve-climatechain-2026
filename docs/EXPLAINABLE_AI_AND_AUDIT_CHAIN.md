# RESERVE explainable decision support and audit-chain design

## Purpose

This implementation adds two prototype components:

1. Explainable multi-criteria decision support in src/reserve/ai_decision.py and POST /api/decision-support.
2. A SHA-256 hash-chained audit log in src/reserve/audit_ledger.py, GET /api/audit, and POST /api/audit/verify.

These are steps toward an AI- and blockchain-enabled climate solution, but their scope must be described accurately.

## Decision-support model

The model first applies the same hard eligibility rules as the ordinary evaluator. Ineligible processors are never scored as recommendations. Eligible candidates are scored on four normalized, visible criteria:

| Criterion | Weight | Meaning |
|---|---:|---|
| Lower estimated transport emissions | 45% | Relative score derived from the supplied factor and shipment distance/quantity |
| Quality margin | 20% | Relative headroom above the required quality threshold |
| Capacity headroom | 20% | Relative available capacity above shipment quantity |
| Delivery-window fit | 15% | Share of requested delivery window overlapped by processor availability |

The weights are demonstration defaults, not fitted from data, stakeholder research, or an operational outcome study. This is a deterministic, explainable multi-criteria decision model—not a trained machine-learning model. Describe it as AI-style decision support or explainable decision support, not a validated predictive AI system. Output is advisory and must not override safety, regulatory, quality, or contractual controls.

When the same illustrative factor is applied to every candidate, the emissions component is effectively a distance ranking. The score is not proof of climate impact. Real deployment requires source-backed, applicable factors and actual activity data.

## Audit-chain model

Each decision-support request appends a JSON Lines record containing schema version and sequential event number; UTC timestamp; previous record's SHA-256 hash; event type and shipment inputs; model identifier and advisory selection; synthetic-data and unverified-emissions disclosures; and a SHA-256 hash of the canonicalized record contents.

The verifier checks event numbering, previous-hash links, and each record's content hash. Altering or removing an interior event should cause verification to fail.

### What this does and does not provide

This is a **local hash-chained audit log**, not a decentralized blockchain. It does not provide distributed consensus, independent validators, replicated storage, identity management, public anchoring, smart contracts, or resistance to a privileged operator replacing the entire ledger. It provides a useful integrity-checking primitive for a prototype and a foundation for future design.

Before describing a production deployment as blockchain-enabled, the project must implement and document the actual network/ledger architecture, validator model, transaction permissions, key management, privacy controls, deployment, and independent verification. A hash chain alone must never be represented as a blockchain.

## Endpoints

### POST /api/decision-support

Accepts material, quantity_tonnes, required_quality, earliest_delivery_day, and latest_delivery_day. Returns model identifier/type, weights, candidate scores, component scores, explanations, limitations, and audit event sequence/hash.

### GET /api/audit and POST /api/audit/verify

Return verification status, event count, chain head, and explicit ledger type/limitations. Verification is read-only.

## Storage and deployment limitations

By default the JSONL file is stored at instance/audit_chain.jsonl, unless RESERVE_AUDIT_LEDGER_PATH is set. Local or ephemeral deployment storage can be lost during redeployment or instance replacement. Multi-worker concurrent writes, network replication, retention, backup, privacy, and tamper resistance against privileged filesystem access require additional engineering before production use.

## Climate evidence boundary

The current profiles are fictional and the fallback factor is illustrative and unsourced. The audit record proves only the integrity of the stored record relative to the current chain; it does not prove that input facts are true. No measured emissions reduction, avoided waste, operational benefit, or climate impact is established. A controlled shadow-mode pilot with source-linked data, pre-registered outcomes, and independent review remains necessary.
