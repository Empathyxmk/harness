import unittest
from src.deye_at_connector import DeyeAtConnector

class TestDeyeAtConnectorPublic(unittest.TestCase):
    def test_device_id_parsing_variation(self):
        # Use a different (public) serial response and device id
        connector = DeyeAtConnector("/dev/null")
        resp = "OK\r\nDEVICE_ID:12345PUBLIC\r\nOK\r\n"
        device_id = connector._parse_device_id_response(resp)
        self.assertEqual(device_id, "12345PUBLIC")

    def test_parse_non_matching_device_id(self):
        connector = DeyeAtConnector("/dev/null")
        resp = "OK\r\nNO_DEVICE\r\nOK\r\n"
        device_id = connector._parse_device_id_response(resp)
        self.assertIsNone(device_id)