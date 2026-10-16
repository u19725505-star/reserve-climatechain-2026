"""Hash-chained local audit ledger for RESERVE demo events.

A hash chain makes edits to recorded events detectable when the chain is
verified. This local file is NOT a decentralized blockchain: it has no
consensus, distributed replication, identity layer, or external anchoring.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENESIS_HASH = "0" * 64
_LOCK = threading.Lock()


def _canonical(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def _event_hash(record_without_hash: dict) -> str:
    return hashlib.sha256(_canonical(record_without_hash)).hexdigest()


def _ledger_path() -> Path:
    return Path(os.environ.get(
        "RESERVE_AUDIT_LEDGER_PATH",
        str(Path(__file__).resolve().parents[2] / "instance" / "audit_chain.jsonl"),
    ))


def append_event(event: dict) -> dict:
    """Append one event linked to the prior event hash."""
    if not isinstance(event, dict) or not event:
        raise ValueError("Event must be a non-empty JSON object.")
    # Validate canonical JSON up front (e.g. rejects NaN and non-JSON values).
    _canonical(event)
    path = _ledger_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        previous = GENESIS_HASH
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    previous = json.loads(line)["event_hash"]
        record = {
            "schema_version": "1.0",
            "sequence": 1 if not path.exists() else sum(
                1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
            ) + 1,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "previous_hash": previous,
            "event": event,
        }
        record["event_hash"] = _event_hash(record)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n")
        return record


def verify_chain() -> dict:
    """Verify sequence, previous-hash links, and each event's content hash."""
    path = _ledger_path()
    if not path.exists():
        return {
            "valid": True, "event_count": 0, "head_hash": GENESIS_HASH,
            "ledger_status": "empty", "ledger_type": "local hash-chained audit log",
        }
    previous = GENESIS_HASH
    count = 0
    try:
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            supplied_hash = record.get("event_hash")
            body = {k: v for k, v in record.items() if k != "event_hash"}
            if record.get("sequence") != count + 1:
                return {"valid": False, "event_count": count, "failed_line": line_number,
                        "reason": "sequence_mismatch", "head_hash": previous}
            if record.get("previous_hash") != previous:
                return {"valid": False, "event_count": count, "failed_line": line_number,
                        "reason": "previous_hash_mismatch", "head_hash": previous}
            if supplied_hash != _event_hash(body):
                return {"valid": False, "event_count": count, "failed_line": line_number,
                        "reason": "event_hash_mismatch", "head_hash": previous}
            previous = supplied_hash
            count += 1
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        return {"valid": False, "event_count": count, "reason": "ledger_parse_error",
                "detail": str(exc), "head_hash": previous}
    return {
        "valid": True, "event_count": count, "head_hash": previous,
        "ledger_status": "verified" if count else "empty",
        "ledger_type": "local hash-chained audit log",
        "limitation": "Not a decentralized blockchain; local storage can be lost or replaced.",
    }
