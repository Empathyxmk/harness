import unittest

class DummySerialPort:
    def __init__(self):
        self.buffer = ""

    def write(self, msg):
        self.buffer += msg

    def read(self):
        if self.buffer == "status\n":
            return "device ok\n"
        elif self.buffer == "value\n":
            return "1234\n"
        else:
            return "?\n"

class TestSerialPublic(unittest.TestCase):
    def setUp(self):
        self.serial = DummySerialPort()

    def test_status_message(self):
        self.serial.write("status\n")
        reply = self.serial.read()
        self.assertEqual(reply, "device ok\n")

    def test_value_message(self):
        self.serial.write("value\n")
        reply = self.serial.read()
        self.assertEqual(reply, "1234\n")

    def test_unknown_message(self):
        self.serial.write("foobar\n")
        reply = self.serial.read()
        self.assertEqual(reply, "?\n")

if __name__ == '__main__':
    unittest.main()