import unittest
import importlib.util
import sys
import os

import maskerlogger.secrets_in_logs_example as si

class TestImportSecretsInLogsExample(unittest.TestCase):
    def test_import_and_main(self):
        # Import shouldn't fail
        si.main()  # Should call log_sensitive, which should not raise

    def test_cmd_main_guard(self):
        # Simulate running as __main__
        module_name = "maskerlogger.secrets_in_logs_example"
        filename = si.__file__
        spec = importlib.util.spec_from_file_location("__main__", filename)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["__main__"] = mod
        try:
            spec.loader.exec_module(mod)
        finally:
            sys.modules.pop("__main__")

    def test_log_sensitive_runs(self):
        si.log_sensitive()

if __name__ == "__main__":
    unittest.main()