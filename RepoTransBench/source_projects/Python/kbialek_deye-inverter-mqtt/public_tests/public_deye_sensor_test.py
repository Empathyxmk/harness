import unittest
from src.deye_sensor import AbstractSensor, SensorRegisterRanges


class DemoSensor(AbstractSensor):
    def __init__(self, name="voltage", value=158.9, is_readiness_check=True):
        super().__init__(name=name, groups=["test"], print_format="{:0.2f}")
        self._value = value
        self._is_readiness_check = is_readiness_check

    def read_value(self, registers):
        return self._value

    @property
    def is_readiness_check(self):
        return self._is_readiness_check


class TestDeyeSensorPublic(unittest.TestCase):

    def test_sensor_read_value(self):
        s = DemoSensor(name="energy", value=321.12)
        self.assertEqual(s.read_value([0]), 321.12)

    def test_register_ranges(self):
        r = SensorRegisterRanges([10, 20], [22, 33], 512)
        self.assertEqual(r.base, 512)
        self.assertListEqual(r.ranges, [10, 20])
        self.assertListEqual(r.input_ranges, [22, 33])

    def test_sensor_str_and_repr(self):
        s = DemoSensor(name="freq", value=1001.1)
        s_repr = repr(s)
        self.assertIn("freq", s_repr)
        self.assertTrue("DemoSensor" in s.__class__.__name__)


if __name__ == "__main__":
    unittest.main()