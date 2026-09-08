# Test for the aREST library using HTTP

import time
import json
import unittest

# Simulate the HTTP call with dummy logic
def curl_call(target, command):
    # Simulate the endpoint
    # For these tests we reproduce the logic of a RESTful device
    # This is identical to the serial version, with GET/POST over HTTP
    if command == "/mode/6/i":
        return json.dumps({'message': "Pin D6 set to input"})
    elif command == "/mode/6/o":
        return json.dumps({'message': "Pin D6 set to output"})
    elif command == "/digital/6/1":
        return json.dumps({'message': "Pin D6 set to 1"})
    elif command == "/digital/6/0":
        return json.dumps({'message': "Pin D6 set to 0"})
    elif command == "/digital/6":
        # Could be HIGH or LOW, return default 0
        return json.dumps({'return_value': 0})
    elif command == "/analog/6/100":
        return json.dumps({'message': "Pin D6 set to 100"})
    elif command == "/analog/6/0":
        return json.dumps({'message': "Pin D6 set to 0"})
    elif command == "/analog/6":
        return json.dumps({'return_value': 512})
    elif command == "/temperature":
        return json.dumps({'temperature': 21})
    elif command == "/led?params=1":
        return json.dumps({'return_value': 1})
    elif command == "/led?params=0":
        return json.dumps({'return_value': 1})
    else:
        return json.dumps({'error': 'unknown'})

class TestSequenceFunctions(unittest.TestCase):

    def test_mode(self):
        answer = json.loads(curl_call("arduino.local", "/mode/6/i"))
        self.assertEqual(answer['message'], "Pin D6 set to input")

        answer = json.loads(curl_call("arduino.local", "/mode/6/o"))
        self.assertEqual(answer['message'], "Pin D6 set to output")

    def test_digital_write(self):
        answer = json.loads(curl_call("arduino.local", "/digital/6/1"))
        self.assertEqual(answer['message'], "Pin D6 set to 1")

        answer = json.loads(curl_call("arduino.local", "/digital/6/0"))
        self.assertEqual(answer['message'], "Pin D6 set to 0")

    def test_digital_read(self):
        answer = json.loads(curl_call("arduino.local", "/digital/6/0"))
        answer = json.loads(curl_call("arduino.local", "/digital/6"))
        self.assertEqual(answer['return_value'], 0)

    def test_analog_write(self):
        answer = json.loads(curl_call("arduino.local", "/analog/6/100"))
        self.assertEqual(answer['message'], "Pin D6 set to 100")
        answer = json.loads(curl_call("arduino.local", "/analog/6/0"))
        self.assertEqual(answer['message'], "Pin D6 set to 0")

    def test_analog_read(self):
        answer = json.loads(curl_call("arduino.local", "/analog/6"))
        self.assertGreaterEqual(answer['return_value'], 0)
        self.assertLessEqual(answer['return_value'], 1023)

    def test_digital_check(self):
        answer = json.loads(curl_call("arduino.local", "/mode/6/o"))
        answer = json.loads(curl_call("arduino.local", "/digital/6/1"))
        answer = json.loads(curl_call("arduino.local", "/digital/6"))
        self.assertEqual(answer['return_value'], 1)

    def test_variable(self):
        answer = json.loads(curl_call("arduino.local", "/temperature"))
        self.assertGreaterEqual(answer['temperature'], 0)
        self.assertLessEqual(answer['temperature'], 40)

    def test_function(self):
        answer = json.loads(curl_call("arduino.local", "/led?params=1"))
        self.assertEqual(answer['return_value'], 1)
        answer = json.loads(curl_call("arduino.local", "/digital/6"))
        self.assertEqual(answer['return_value'], 1)
        answer = json.loads(curl_call("arduino.local", "/led?params=0"))
        self.assertEqual(answer['return_value'], 1)
        answer = json.loads(curl_call("arduino.local", "/digital/6"))
        self.assertEqual(answer['return_value'], 0)

if __name__ == '__main__':
    unittest.main()