import unittest

class TriggerMode:
    AUTO = 0
    NORMAL = 1
    SINGLE = 2

    @staticmethod
    def is_valid(mode):
        return mode in (TriggerMode.AUTO, TriggerMode.NORMAL, TriggerMode.SINGLE)

class TestTriggerModePublic(unittest.TestCase):
    def test_valid_modes(self):
        for valid_mode in [TriggerMode.SINGLE, TriggerMode.NORMAL, TriggerMode.AUTO]:
            self.assertTrue(TriggerMode.is_valid(valid_mode))

    def test_invalid_mode(self):
        self.assertFalse(TriggerMode.is_valid(99))
        self.assertFalse(TriggerMode.is_valid(-10))
        self.assertFalse(TriggerMode.is_valid(None))

if __name__ == "__main__":
    unittest.main()