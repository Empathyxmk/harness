import unittest
import json

class DummyRestClient:
    def __init__(self):
        self.state = {}
        self.last_pin = None

    def get(self, endpoint):
        if endpoint == "/digitalRead/3":
            return json.dumps({"return_value": 1})
        if endpoint == "/analogRead/5":
            return json.dumps({"return_value": 123})
        return json.dumps({"return_value": -1})

    def post(self, endpoint, data):
        if endpoint == "/digitalWrite/3":
            self.state[3] = data
            self.last_pin = 3
            return json.dumps({"return_value": data})
        if endpoint == "/analogWrite/5":
            self.state[5] = data
            self.last_pin = 5
            return json.dumps({"return_value": data})
        return json.dumps({"return_value": -1})

class TestLightweightPublic(unittest.TestCase):
    def setUp(self):
        self.client = DummyRestClient()

    def test_digital_read(self):
        resp = json.loads(self.client.get("/digitalRead/3"))
        self.assertEqual(resp["return_value"], 1)

    def test_analog_read(self):
        resp = json.loads(self.client.get("/analogRead/5"))
        self.assertEqual(resp["return_value"], 123)

    def test_digital_write(self):
        resp = json.loads(self.client.post("/digitalWrite/3", 0))
        self.assertEqual(resp["return_value"], 0)
        self.assertEqual(self.client.state[3], 0)

    def test_analog_write(self):
        resp = json.loads(self.client.post("/analogWrite/5", 88))
        self.assertEqual(resp["return_value"], 88)
        self.assertEqual(self.client.state[5], 88)

if __name__ == '__main__':
    unittest.main()