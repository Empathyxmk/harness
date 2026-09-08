import unittest
import random

class RESTStressClient:
    def __init__(self):
        self.stress_counter = 0

    def request(self, endpoint):
        if endpoint.startswith("/digitalRead/"):
            val = random.choice([0, 1])
            self.stress_counter += 1
            return {"return_value": val}
        elif endpoint.startswith("/analogRead/"):
            val = (self.stress_counter * 2 + 10) % 1024
            self.stress_counter += 1
            return {"return_value": val}
        return {"error": "unknown"}

class PublicStressTest(unittest.TestCase):
    def setUp(self):
        self.client = RESTStressClient()

    def test_multiple_digital_reads(self):
        values = [self.client.request(f"/digitalRead/{i}")["return_value"] for i in range(20)]
        self.assertTrue(all(v in [0, 1] for v in values))

    def test_multiple_analog_reads(self):
        results = []
        for i in range(20, 40):
            resp = self.client.request(f"/analogRead/{i}")
            results.append(resp["return_value"])
        self.assertTrue(all(isinstance(rv, int) and (10 <= rv < 1024) for rv in results))

if __name__ == '__main__':
    unittest.main()