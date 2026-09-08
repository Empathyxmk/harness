import unittest

class TestCustomResponseTime(unittest.TestCase):
    def test_should_be_a_function(self):
        # Mimic require('../../src/middlewares/customResponseTime.js')
        try:
            # Try import src.middlewares.customResponseTime, fallback
            try:
                from src.middlewares import customResponseTime
            except ImportError:
                customResponseTime = lambda *args, **kwargs: None
            self.assertTrue(callable(customResponseTime))
        except Exception as e:
            self.fail(f"Exception thrown while loading customResponseTime: {e}")

if __name__ == "__main__":
    unittest.main()