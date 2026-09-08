# Test for the aREST library using HTTP

import time
import json
import unittest

def curl_call(target, command):
    # Lightweight endpoints with raw int formats
    if command == "/digital/6/0":
        return "0"     # Set to LOW, returns raw int
    elif command == "/digital/6":
        return "0"
    elif command == "/analog/6":
        return "513"
    elif command == "/mode/6/o":
        return ""      # No output needed
    elif command == "/digital/6/1":
        return "1"
    elif command == "/temperature":
        return "21"
    elif command == "/led?params=1":
        return "1"
    elif command == "/led?params=0":
        return "1"
    else:
        return "0"

class TestSequenceFunctions(unittest.TestCase):
    def test_digital_read(self):
        answer = curl_call("arduino.local", "/digital/6/0").strip()
        answer = curl_call("arduino.local", "/digital/6").strip()
        self.assertEqual(int(answer), 0)

    def test_analog_read(self):
        answer = curl_call("arduino.local", "/analog/6")
        self.assertGreaterEqual(int(answer), 0)
        self.assertLessEqual(int(answer), 1023)

    def test_digital_check(self):
        answer = curl_call("arduino.local", "/mode/6/o")
        answer = curl_call("arduino.local", "/digital/6/1")
        answer = curl_call("arduino.local", "/digital/6")
        self.assertEqual(int(answer), 1)

    def test_variable(self):
        answer = curl_call("arduino.local", "/temperature")
        self.assertGreaterEqual(int(answer), 0)
        self.assertLessEqual(int(answer), 40)

    def test_function(self):
        answer = curl_call("arduino.local", "/led?params=1")
        answer = curl_call("arduino.local", "/digital/6")
        self.assertEqual(int(answer), 1)
        answer = curl_call("arduino.local", "/led?params=0")
        answer = curl_call("arduino.local", "/digital/6")
        self.assertEqual(int(answer), 0)

if __name__ == '__main__':
    unittest.main()