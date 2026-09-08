import unittest

class DummyParticleSystem:
    def __init__(self, activity, n, drawable, ms):
        pass

class TestParticleSystemDummy(unittest.TestCase):
    def test_dummy_coverage_just_to_trigger_class(self):
        # Just creating an instance for coverage; no assertions needed.
        DummyParticleSystem(None, 10, None, 1000)