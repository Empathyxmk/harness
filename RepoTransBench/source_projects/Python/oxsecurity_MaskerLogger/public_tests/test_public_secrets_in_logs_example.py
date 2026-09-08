import unittest
import logging
from maskerlogger.masker_formatter import MaskerFormatter

def log_sensitive_public():
    logger = logging.getLogger("test_logger_public")
    handler = logging.StreamHandler()
    handler.setFormatter(MaskerFormatter("%(message)s", regex_config_path=None))
    logger.addHandler(handler)
    logger.setLevel(logging.WARNING)
    logger.warning("secret field: thisshouldberedacted321 must be hidden")
    logger.warning("nondescript info log")
    logger.warning("skip me", extra={"apply_mask": False})
    logger.removeHandler(handler)

class TestSecretsInLogsExamplePublic(unittest.TestCase):
    def test_log_sensitive_public_runs(self):
        # Just ensure it runs as it is a demonstration
        log_sensitive_public()

if __name__ == "__main__":
    unittest.main()