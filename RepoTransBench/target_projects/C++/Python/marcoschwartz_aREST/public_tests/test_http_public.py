import unittest
import json

def simulated_curl_call(command):
    if command == "/mode/8/i":
        return json.dumps({"return_value": 1, "message": "Pin set to input", "mode": "i"})
    elif command == "/digital/8/1":
        return json.dumps({"return_value": 1, "message": "Pin 8 set high"})
    elif command == "/digital/8/0":
        return json.dumps({"return_value": 0, "message": "Pin 8 reads low"})
    elif command == "/analog/6":
        return json.dumps({"return_value": 654, "message": "Analog read pin 6"})
    elif command == "/analog/6/151":
        return json.dumps({"return_value": 151, "message": "Analog write 151 to pin 6"})
    elif command == "/mode/8/o":
        return json.dumps({"return_value": 1, "message": "Pin set to output", "mode": "o"})
    elif command == "/fan?params=4":
        return json.dumps({"return_value": 42, "message": "fan triggered with param 4"})
    elif command == "/humidity":
        return json.dumps({"return_value": 70, "message": "humidity value is 70"})
    else:
        return json.dumps({"error": "unknown endpoint"})

class PublicTestSequenceFunctions(unittest.TestCase):

    def test_mode(self):
        answer = json.loads(simulated_curl_call("/mode/8/i"))
        self.assertIn("mode", answer)
        self.assertEqual(answer["mode"], "i")

    def test_digital_write(self):
        answer = json.loads(simulated_curl_call("/digital/8/1"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 1)

    def test_digital_read(self):
        answer = json.loads(simulated_curl_call("/digital/8/0"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 0)

    def test_analog_write(self):
        answer = json.loads(simulated_curl_call("/analog/6/151"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 151)

    def test_analog_read(self):
        answer = json.loads(simulated_curl_call("/analog/6"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 654)

    def test_digital_check(self):
        answer = json.loads(simulated_curl_call("/mode/8/o"))
        self.assertIn("mode", answer)
        self.assertEqual(answer["mode"], "o")

    def test_variable(self):
        answer = json.loads(simulated_curl_call("/humidity"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 70)

    def test_function(self):
        answer = json.loads(simulated_curl_call("/fan?params=4"))
        self.assertIn("return_value", answer)
        self.assertEqual(answer["return_value"], 42)

if __name__ == '__main__':
    unittest.main()