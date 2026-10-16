"""Smoke tests for the standalone RESERVE demonstration."""

import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path

from reserve.demo import main


class TestDemoCLI(unittest.TestCase):
    def test_demo_runs_and_writes_machine_readable_results(self):
        original_cwd = Path.cwd()
        with tempfile.TemporaryDirectory() as temp_dir:
            try:
                os.chdir(temp_dir)
                output = io.StringIO()
                with contextlib.redirect_stdout(output):
                    main()
                result_path = Path(temp_dir) / "results" / "processor_comparison.json"
                self.assertTrue(result_path.is_file())
                self.assertIn("fictional", output.getvalue().lower())
                self.assertIn("illustrative", output.getvalue().lower())
            finally:
                os.chdir(original_cwd)


if __name__ == "__main__":
    unittest.main()
