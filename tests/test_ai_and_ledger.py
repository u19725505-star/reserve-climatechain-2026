import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from unittest.mock import patch

from reserve.audit_ledger import append_event, verify_chain
from reserve.ai_decision import score_eligible_processors
from reserve.demo_data import ILLUSTRATIVE_FACTOR, demo_processors
from reserve.evaluation import Shipment


class TestExplainableDecisionModel(unittest.TestCase):
    def setUp(self):
        self.shipment = Shipment("recycled_plastic", 7, 0.8, 5, 8)

    def test_scores_only_eligible_candidates_and_explains_weights(self):
        result = score_eligible_processors(
            self.shipment, demo_processors(), ILLUSTRATIVE_FACTOR
        )
        self.assertEqual(result["status"], "advisory_only")
        self.assertEqual({x["processor"] for x in result["candidates"]},
                         {"Processor A", "Processor B"})
        self.assertAlmostEqual(sum(result["weights"].values()), 1.0)
        self.assertIn("not trained", " ".join(result["limitations"]))

    def test_no_eligible_candidates_is_explicit(self):
        shipment = Shipment("recycled_plastic", 30, 0.8, 5, 8)
        result = score_eligible_processors(
            shipment, demo_processors(), ILLUSTRATIVE_FACTOR
        )
        self.assertEqual(result["status"], "no_eligible_candidates")
        self.assertEqual(result["candidates"], [])


class TestHashChainedAuditLedger(unittest.TestCase):
    def test_append_and_verify_and_detect_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "ledger.jsonl")
            with patch.dict(os.environ, {"RESERVE_AUDIT_LEDGER_PATH": path}):
                first = append_event({"type": "routing_decision", "selected": "Processor B"})
                second = append_event({"type": "outcome", "status": "pending"})
                self.assertEqual(first["sequence"], 1)
                self.assertEqual(second["sequence"], 2)
                self.assertEqual(second["previous_hash"], first["event_hash"])
                self.assertTrue(verify_chain()["valid"])
                records = open(path, encoding="utf-8").readlines()
                altered = json.loads(records[0])
                altered["event"]["selected"] = "Processor A"
                records[0] = json.dumps(altered) + "\n"
                open(path, "w", encoding="utf-8").writelines(records)
                result = verify_chain()
                self.assertFalse(result["valid"])
                self.assertIn(result["reason"], {"event_hash_mismatch", "previous_hash_mismatch"})



class TestDecisionSupportAPI(unittest.TestCase):
    def test_api_returns_explanations_and_audit_hash(self):
        from app import app
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"RESERVE_AUDIT_LEDGER_PATH": os.path.join(tmp, "api.jsonl")}):
                client = app.test_client()
                response = client.post("/api/decision-support", json={
                    "material": "recycled_plastic", "quantity_tonnes": 7,
                    "required_quality": 0.8, "earliest_delivery_day": 5,
                    "latest_delivery_day": 8,
                })
                self.assertEqual(response.status_code, 200)
                body = response.get_json()
                self.assertEqual(body["model"], "RESERVE-XAI-MCDM-0.1")
                self.assertEqual(body["status"], "advisory_only")
                self.assertTrue(body["candidates"])
                self.assertEqual(body["audit"]["event_sequence"], 1)
                self.assertEqual(len(body["audit"]["event_hash"]), 64)
                self.assertTrue(client.get("/api/audit").get_json()["valid"])

    def test_audit_api_reports_empty_chain(self):
        from app import app
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {"RESERVE_AUDIT_LEDGER_PATH": os.path.join(tmp, "empty.jsonl")}):
                body = app.test_client().get("/api/audit").get_json()
                self.assertTrue(body["valid"])
                self.assertEqual(body["event_count"], 0)


if __name__ == "__main__":
    unittest.main()
