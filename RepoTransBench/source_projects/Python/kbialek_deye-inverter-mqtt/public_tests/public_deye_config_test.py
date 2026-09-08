import unittest
from src.deye_config import DeyeMqttConfig


class TestDeyeConfigPublic(unittest.TestCase):

    def test_mqtt_config_repr_and_eq(self):
        cfg1 = DeyeMqttConfig(
            host="127.0.0.3",
            port=1337,
            username="alpha",
            password="beta",
            topic_prefix="solar/"
        )
        cfg2 = DeyeMqttConfig(
            host="127.0.0.3",
            port=1337,
            username="alpha",
            password="beta",
            topic_prefix="solar/"
        )
        cfg3 = DeyeMqttConfig(
            host="192.168.0.8",
            port=833,
            username="a",
            password="b",
            topic_prefix="power/"
        )
        self.assertEqual(cfg1, cfg2)
        self.assertNotEqual(cfg1, cfg3)
        self.assertIn("DeyeMqttConfig", repr(cfg1))
        self.assertIn("solar", repr(cfg1))


if __name__ == "__main__":
    unittest.main()