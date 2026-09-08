import unittest

class TargetInfo:
    def __init__(self, hostname, port, password):
        self.hostname = hostname
        self.port = port
        self.password = password

class TestPublicTargetInfo(unittest.TestCase):
    def test_public_basic_values(self):
        info = TargetInfo("10.2.3.4", 4321, "PUBPASS")
        self.assertEqual(info.hostname, "10.2.3.4")
        self.assertEqual(info.port, 4321)
        self.assertEqual(info.password, "PUBPASS")