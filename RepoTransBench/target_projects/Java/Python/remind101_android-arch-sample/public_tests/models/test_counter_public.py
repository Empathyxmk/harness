import unittest

class Counter:
    _next_id = 1
    def __init__(self):
        self._id = Counter._next_id
        Counter._next_id += 1
        self._value = 0

    def getValue(self):
        return self._value

    def setValue(self, v):
        self._value = v

    def getId(self):
        return self._id

    def increment(self):
        self._value += 1

    def decrement(self):
        self._value -= 1

class TestCounterPublic(unittest.TestCase):
    def testCounterIncrementPublic(self):
        counter = Counter()
        oldValue = counter.getValue()
        counter.increment()
        self.assertEqual(oldValue + 1, counter.getValue())

    def testCounterDecrementPublic(self):
        counter = Counter()
        counter.setValue(78)
        counter.decrement()
        self.assertEqual(77, counter.getValue())

    def testCounterSetValueAndGetIdPublic(self):
        counter = Counter()
        counter.setValue(1234)
        self.assertEqual(1234, counter.getValue())
        self.assertTrue(counter.getId() > 0)

if __name__ == "__main__":
    unittest.main()