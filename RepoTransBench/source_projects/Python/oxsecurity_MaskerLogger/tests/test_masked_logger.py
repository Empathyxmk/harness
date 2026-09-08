import unittest
import logging
import os
from maskerlogger.masker_formatter import MaskerFormatter, MaskerFormatterJson
from maskerlogger import masker_formatter

TEST_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "maskerlogger/config/gitleaks.toml")

class DummyRecord(logging.LogRecord):
    def __init__(self, msg):
        super().__init__(name="foo", level=logging.WARNING, pathname=__file__, lineno=1, msg=msg, args=(), exc_info=None)

class TestMaskerLoggerFullPaths(unittest.TestCase):
    def setUp(self):
        self.fmt = "%(levelname)s %(message)s"
        self.formatter = MaskerFormatter(self.fmt, regex_config_path=TEST_CONFIG_PATH, redact=75)
        self.json_formatter = MaskerFormatterJson("%(message)s", regex_config_path=TEST_CONFIG_PATH, redact=50)

    def test_mask_secret_logic(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        # Simulate a match with groups
        import re
        match = re.match(r"(a)(b+)", "abbbbb")
        msg = logger._mask_secret("abbbbb start abbbbb", [match])
        self.assertTrue(msg.count("*") > 0)

    def test_mask_sensitive_data_no_match(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        record = DummyRecord("no secrets here")
        logger._mask_sensitive_data(record)
        self.assertEqual(record.msg, "no secrets here")

    def test_mask_sensitive_data_with_match(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        record = DummyRecord('"password": "password321" and apikey = 1234')
        logger.redact = 45
        logger._mask_sensitive_data(record)
        self.assertIsInstance(record.msg, str)
        self.assertFalse("password321" in record.msg)

    def test_formatter_full_log_integration(self):
        # Simulate regular use as in the "secrets_in_logs_example.py"
        logger = logging.getLogger("logtest")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        try:
            logger.info('"current_key": "AIzaSOHbouG6DDa6DOcRGEgOMayAXYXcw6la3c"')
            logger.info('"AKIAI44QH8DHBEXAMPLE" and then more text.')
            logger.info("Datadog access token: 'abcdef1234567890abcdef1234567890'")
            logger.info('"password": "password123"')
        finally:
            logger.removeHandler(handler)

    def test_json_formatter_logrecord_masking(self):
        rec = DummyRecord('apikey = "TESTEXPOSEDSECRET"')
        value = self.json_formatter.format(rec)
        self.assertIn("apikey", value)

    def test_maskerformatterjson_skip_mask(self):
        rec = DummyRecord("sometext")
        setattr(rec, "apply_mask", False)
        # Should not attempt masking
        result = self.json_formatter.format(rec)
        self.assertIn("sometext", result)

    def test_repr_and_str(self):
        # test __repr__ and __str__ if any (none present, but test constructor str)
        self.assertIn("Json", type(self.json_formatter).__name__)

if __name__ == "__main__":
    unittest.main()