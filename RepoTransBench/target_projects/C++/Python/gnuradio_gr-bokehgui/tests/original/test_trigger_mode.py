import unittest

class TriggerMode:
    AUTO = 0
    NORMAL = 1
    SINGLE = 2

    @staticmethod
    def is_valid(mode):
        return mode in (TriggerMode.AUTO, TriggerMode.NORMAL, TriggerMode.SINGLE)

class TestTriggerMode(unittest.TestCase):
    def test_valid_modes(self):
        self.assertTrue(TriggerMode.is_valid(TriggerMode.AUTO))
        self.assertTrue(TriggerMode.is_valid(TriggerMode.NORMAL))
        self.assertTrue(TriggerMode.is_valid(TriggerMode.SINGLE))

    def test_invalid_mode(self):
        self.assertFalse(TriggerMode.is_valid(3))
        self.assertFalse(TriggerMode.is_valid(-1))
        self.assertFalse(TriggerMode.is_valid('AUTO'))

if __name__ == "__main__":
    unittest.main()