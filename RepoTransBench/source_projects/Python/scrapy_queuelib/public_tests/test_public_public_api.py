import unittest
import queuelib

class TestPublicApiPublic(unittest.TestCase):
    def test_module_version_present_public(self):
        self.assertTrue(hasattr(queuelib, "__version__") or hasattr(queuelib, "version"))
        # Check that version string looks like at least two components separated by '.'
        version = getattr(queuelib, "__version__", None) or getattr(queuelib, "version", None)
        if version is not None:
            self.assertIn('.', version)

    def test_module_has_pqueue_and_rrqueue_public(self):
        self.assertTrue(hasattr(queuelib, "pqueue"))
        self.assertTrue(hasattr(queuelib, "rrqueue"))
        # Check that both provide a PriorityQueue or RoundRobinQueue class
        self.assertTrue(hasattr(queuelib.pqueue, "PriorityQueue"))
        self.assertTrue(hasattr(queuelib.rrqueue, "RoundRobinQueue"))

if __name__ == "__main__":
    unittest.main()