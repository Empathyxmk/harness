import unittest

class Counter:
    def __init__(self):
        self._id = 0
        self._value = 0
    def getId(self):
        return self._id
    def setId(self, id):
        self._id = id
    def getValue(self):
        return self._value
    def setValue(self, v):
        self._value = v

class TestCounter(unittest.TestCase):
    def testCounterDefaultConstructorAndValue(self):
        counter = Counter()
        self.assertEqual(0, counter.getId())
        self.assertEqual(0, counter.getValue())

    def testCounterSetAndGetId(self):
        counter = Counter()
        counter.setId(123)
        self.assertEqual(123, counter.getId())

    def testCounterSetAndGetValue(self):
        counter = Counter()
        counter.setValue(10)
        self.assertEqual(10, counter.getValue())

if __name__ == "__main__":
    unittest.main()