import json
import os
import tempfile
import unittest
from unittest.mock import patch

from src.reserve.audit_ledger import append_event, verify_chain
from src.reserve.ai_decision import score_eligible_processors
from src.reserve.demo_data import ILLUSTRATIVE_FACTOR, demo_processors
from src.reserve.evaluation import Shipment


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


if __name__ == "__main__":
    unittest.main()
