import unittest
import logging
from maskerlogger.masker_formatter import MaskerFormatter, MaskerFormatterJson, AbstractMaskedLogger, SKIP_MASK

class DummyRecord(logging.LogRecord):
    def __init__(self, msg):
        super().__init__("foo", logging.INFO, __file__, 1, msg, (), None)

class TestMaskerFormatter(unittest.TestCase):
    def test_no_masking_if_no_match(self):
        formatter = MaskerFormatter("%(message)s", regex_config_path=None)
        rec = DummyRecord("nothing secret here")
        out = formatter.format(rec)
        self.assertEqual(out, "nothing secret here")

    def test_masking_with_regex_match(self):
        formatter = MaskerFormatter("%(message)s", regex_config_path=None)
        rec = DummyRecord("password: hunter2")
        out = formatter.format(rec)
        self.assertIn("***", out)

    def test_skip_mask(self):
        formatter = MaskerFormatterJson("%(message)s")
        rec = DummyRecord("skip masking please")
        setattr(rec, "apply_mask", False)
        out = formatter.format(rec)
        self.assertEqual(out, "skip masking please")

class TestAbstractMaskedLogger(unittest.TestCase):
    def test_mask_secret(self):
        logger = AbstractMaskedLogger(regex_config_path=None)
        import re
        m = re.search(r"(hunter2)", "password: hunter2")
        masked = logger._mask_secret("password: hunter2", [m])
        self.assertIn("***", masked)

if __name__ == "__main__":
    unittest.main()