import unittest
import logging
from maskerlogger.masker_formatter import MaskerFormatter, MaskerFormatterJson, AbstractMaskedLogger

class DummyRecord(logging.LogRecord):
    def __init__(self, msg):
        super().__init__("dummy", logging.WARNING, __file__, 4, msg, (), None)

class TestMaskerFormatterPublic(unittest.TestCase):
    def test_no_masking_if_no_match_public(self):
        formatter = MaskerFormatter("%(message)s", regex_config_path=None)
        rec = DummyRecord("12345 is a safe message")
        out = formatter.format(rec)
        self.assertEqual(out, "12345 is a safe message")

    def test_masking_with_regex_match_public(self):
        formatter = MaskerFormatter("%(message)s", regex_config_path=None)
        rec = DummyRecord("apikey: mytopsecret")
        out = formatter.format(rec)
        self.assertIn("***", out)

    def test_skip_mask_public(self):
        formatter = MaskerFormatterJson("%(message)s")
        rec = DummyRecord("nothing to mask here")
        setattr(rec, "apply_mask", False)
        out = formatter.format(rec)
        self.assertEqual(out, "nothing to mask here")

class TestAbstractMaskedLoggerPublic(unittest.TestCase):
    def test_mask_secret_public(self):
        logger = AbstractMaskedLogger(regex_config_path=None)
        import re
        m = re.search(r"(mytopsecret)", "apikey: mytopsecret")
        masked = logger._mask_secret("apikey: mytopsecret", [m])
        self.assertIn("***", masked)

if __name__ == "__main__":
    unittest.main()