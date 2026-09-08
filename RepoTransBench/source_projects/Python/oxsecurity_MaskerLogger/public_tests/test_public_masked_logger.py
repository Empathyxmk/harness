import unittest
import logging
import os
from maskerlogger.masker_formatter import MaskerFormatter, MaskerFormatterJson
from maskerlogger import masker_formatter

TEST_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "maskerlogger/config/gitleaks.toml")

class DummyRecord(logging.LogRecord):
    def __init__(self, msg):
        super().__init__(name="dummy", level=logging.ERROR, pathname=__file__, lineno=2, msg=msg, args=(), exc_info=None)

class TestMaskerLoggerFullPathsPublic(unittest.TestCase):
    def setUp(self):
        self.fmt = "%(levelname)s: %(message)s"
        self.formatter = MaskerFormatter(self.fmt, regex_config_path=TEST_CONFIG_PATH, redact=33)
        self.json_formatter = MaskerFormatterJson("%(message)s", regex_config_path=TEST_CONFIG_PATH, redact=22)

    def test_mask_secret_logic_with_new_pattern(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        # Simulate a different match with groups
        import re
        match = re.match(r"(x)(y+)", "xyyyy")
        msg = logger._mask_secret("xyyyy abc xyyyy", [match])
        self.assertTrue(msg.count("*") > 0)
    
    def test_mask_sensitive_data_no_match_newmsg(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        record = DummyRecord("totally safe entry")
        logger._mask_sensitive_data(record)
        self.assertEqual(record.msg, "totally safe entry")

    def test_mask_sensitive_data_with_match_newsecret(self):
        logger = masker_formatter.AbstractMaskedLogger(TEST_CONFIG_PATH)
        record = DummyRecord('"token": "abcd12345efgh" and secret_key = zyxw')
        logger.redact = 39
        logger._mask_sensitive_data(record)
        self.assertIsInstance(record.msg, str)
        self.assertFalse("abcd12345efgh" in record.msg)

    def test_formatter_full_log_integration_public(self):
        logger = logging.getLogger("logtest_public")
        logger.setLevel(logging.ERROR)
        handler = logging.StreamHandler()
        handler.setFormatter(self.formatter)
        logger.addHandler(handler)
        try:
            logger.error('"another_key": "AIzaSoMEoth3rKEY344sdlGh289Ka3dLPd"')
            logger.error('"AWS_SECRET_THISISFAKE" and some more.')
            logger.error("Datadog token is: 'zyxw9876zyxw9876zyxw9876zyxw9876'")
            logger.error('"pin": "5678"')
        finally:
            logger.removeHandler(handler)

    def test_json_formatter_logrecord_masking_public(self):
        rec = DummyRecord('auth = "FAKENEWSECRETXYZ"')
        value = self.json_formatter.format(rec)
        self.assertIn("auth", value)

    def test_maskerformatterjson_skip_mask_public(self):
        rec = DummyRecord("publiclogtext")
        setattr(rec, "apply_mask", False)
        result = self.json_formatter.format(rec)
        self.assertIn("publiclogtext", result)

    def test_repr_and_str_public(self):
        self.assertIn("Json", type(self.json_formatter).__name__)

if __name__ == "__main__":
    unittest.main()