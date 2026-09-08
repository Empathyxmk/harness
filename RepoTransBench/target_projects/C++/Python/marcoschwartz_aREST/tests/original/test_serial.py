# Test for the aREST library using Serial

import time
import json
import unittest

# For the translation, we will mock the serial.Serial object
class DummySerial:
    def __init__(self):
        self._last_cmd = ""
        self._digital_state = {}
        self._analog_state = {}
        self._temperature = 21
        self._pin_mode = {}
    def write(self, msg):
        self._last_cmd = msg.strip()
    def readline(self):
        cmd = self._last_cmd
        if cmd.startswith("/mode/6/i"):
            self._pin_mode[6] = "input"
            return json.dumps({'message': "Pin D6 set to input"})
        elif cmd.startswith("/mode/6/o"):
            self._pin_mode[6] = "output"
            return json.dumps({'message': "Pin D6 set to output"})
        elif cmd.startswith("/digital/6/1"):
            self._digital_state[6] = 1
            return json.dumps({'message': "Pin D6 set to 1"})
        elif cmd.startswith("/digital/6/0"):
            self._digital_state[6] = 0
            return json.dumps({'message': "Pin D6 set to 0"})
        elif cmd == "/digital/6":
            val = self._digital_state.get(6, 0)
            return json.dumps({'return_value': val})
        elif cmd.startswith("/analog/6/"):
            val = int(cmd.split('/')[-1])
            self._analog_state[6] = val
            return json.dumps({'message': f"Pin D6 set to {val}"})
        elif cmd == "/analog/6":
            val = self._analog_state.get(6, 0)
            return json.dumps({'return_value': max(0, min(val, 1023))})
        elif cmd == "/temperature":
            return json.dumps({'temperature': self._temperature})
        elif cmd.startswith("/led?params=1"):
            self._digital_state[6] = 1
            return json.dumps({'return_value': 1})
        elif cmd.startswith("/led?params=0"):
            self._digital_state[6] = 0
            return json.dumps({'return_value': 1})
        else:
            return json.dumps({'error': 'unknown'})

    def reset_input_buffer(self):
        pass
    def reset_output_buffer(self):
        pass

serial_speed = 115200
serial_port = '/dev/tty.usbmodem1a12121'

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.serial = DummySerial()
        time.sleep(0.01)
        self.serial.write("\r\r")
        time.sleep(0.01)
        self.serial.reset_input_buffer()
        self.serial.reset_output_buffer()

    def test_mode(self):
        self.serial.write("/mode/6/i\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to input")

        self.serial.write("/mode/6/o\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to output")

    def test_digital_write(self):
        self.serial.write("/digital/6/1\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to 1")

        self.serial.write("/digital/6/0\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to 0")

    def test_digital_read(self):
        self.serial.write("/digital/6/0\r")
        _ = json.loads(self.serial.readline())
        self.serial.write("/digital/6\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 0)

    def test_analog_write(self):
        self.serial.write("/analog/6/100\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to 100")
        self.serial.write("/analog/6/0\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['message'], "Pin D6 set to 0")

    def test_analog_read(self):
        self.serial.write("/analog/6\r")
        answer = json.loads(self.serial.readline())
        self.assertGreaterEqual(answer['return_value'], 0)
        self.assertLessEqual(answer['return_value'], 1023)

    def test_digital_check(self):
        self.serial.write("/mode/6/o\r")
        _ = json.loads(self.serial.readline())
        self.serial.write("/digital/6/1\r")
        _ = json.loads(self.serial.readline())

        self.serial.write("/digital/6\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 1)

    def test_variable(self):
        self.serial.write("/temperature\r")
        answer = json.loads(self.serial.readline())
        self.assertGreaterEqual(answer['temperature'], 0)
        self.assertLessEqual(answer['temperature'], 40)

    def test_function(self):
        self.serial.write("/led?params=1\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 1)
        self.serial.write("/digital/6\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 1)
        self.serial.write("/led?params=0\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 1)
        self.serial.write("/digital/6\r")
        answer = json.loads(self.serial.readline())
        self.assertEqual(answer['return_value'], 0)

if __name__ == '__main__':
    unittest.main()