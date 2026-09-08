import unittest

class Counter:
    _next_id = 1
    def __init__(self):
        self._id = Counter._next_id
        Counter._next_id += 1
        self._value = 0
    def setValue(self, value):
        self._value = value
    def getValue(self):
        return self._value
    def setId(self, new_id):
        self._id = new_id
    def getId(self):
        return self._id

class CounterDatabase:
    _instance = None
    def __init__(self):
        self.counters = {}

    @classmethod
    def getInstance(cls):
        if not cls._instance:
            cls._instance = CounterDatabase()
        return cls._instance

    def saveCounter(self, counter):
        self.counters[counter.getId()] = counter

    def getCounter(self, cid):
        return self.counters.get(cid, None)

    def getAllCounters(self):
        return list(self.counters.values())

import pytest

class TestCounterDatabase(unittest.TestCase):
    def setUp(self):
        CounterDatabase._instance = None
        Counter._next_id = 1
        self.database = CounterDatabase.getInstance()
        self.database.counters.clear()

    def testGetInstanceSingleton(self):
        db2 = CounterDatabase.getInstance()
        self.assertIs(self.database, db2)

    def testSaveAndGetCounter(self):
        counter = Counter()
        counter.setValue(15)
        self.database.saveCounter(counter)
        result = self.database.getCounter(counter.getId())
        self.assertIsNotNone(result)
        self.assertEqual(counter.getId(), result.getId())
        self.assertEqual(15, result.getValue())

    def testGetCounterNotFound(self):
        c = self.database.getCounter(-1)
        self.assertIsNone(c)

    def testGetAllCounters(self):
        counter1 = Counter()
        counter1.setValue(5)
        self.database.saveCounter(counter1)

        counter2 = Counter()
        counter2.setValue(11)
        self.database.saveCounter(counter2)

        lst = self.database.getAllCounters()
        self.assertTrue(len(lst) >= 2)
        self.assertTrue(all(c.getId() > 0 for c in lst))

if __name__ == "__main__":
    unittest.main()