import unittest

class RCONPacket:
    def __init__(self):
        self.id = 0
        self.type = 0
        self.body = ""

class TestPublicRCON(unittest.TestCase):
    def test_public_rcon_packet_setters_getters(self):
        pkt = RCONPacket()
        pkt.id = 222
        pkt.type = 2
        pkt.body = "PUB BODY"
        self.assertEqual(pkt.id, 222)
        self.assertEqual(pkt.type, 2)
        self.assertEqual(pkt.body, "PUB BODY")