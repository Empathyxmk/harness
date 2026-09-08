import unittest
import os
from queuelib.queue import FifoDiskQueue, LifoDiskQueue

class TestFifoDiskQueuePublic(unittest.TestCase):
    def setUp(self):
        self.path = "test_fifo_disk_public"
        if os.path.exists(self.path):
            os.remove(self.path)
        self.q = FifoDiskQueue(self.path)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.path):
            os.remove(self.path)
    def test_fifo_disk_alternate(self):
        self.q.push(b"w")
        self.q.push(b"x")
        self.assertEqual(self.q.pop(), b"w")
        self.q.push(b"y")
        self.assertEqual(self.q.pop(), b"x")
        self.assertEqual(self.q.pop(), b"y")
        self.assertIsNone(self.q.pop())

class TestLifoDiskQueuePublic(unittest.TestCase):
    def setUp(self):
        self.path = "test_lifo_disk_public"
        if os.path.exists(self.path):
            os.remove(self.path)
        self.q = LifoDiskQueue(self.path)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.path):
            os.remove(self.path)
    def test_lifo_disk_different(self):
        self.q.push(b"x")
        self.q.push(b"y")
        self.q.push(b"z")
        self.assertEqual(self.q.pop(), b"z")
        self.assertEqual(self.q.pop(), b"y")
        self.assertEqual(self.q.pop(), b"x")
        self.assertIsNone(self.q.pop())

@unittest.skip("FifoSQLiteQueue not available in queuelib.queue")
class TestFifoSQLiteQueuePublic(unittest.TestCase):
    def setUp(self):
        self.dbfile = "test_fifo_sqlite_public.db"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
        from queuelib.queue import FifoSQLiteQueue
        self.q = FifoSQLiteQueue("sqlite:///" + self.dbfile)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
    def test_fifo_sqlite_different(self):
        self.q.push(b"data1")
        self.q.push(b"data2")
        self.assertEqual(self.q.pop(), b"data1")
        self.assertEqual(self.q.pop(), b"data2")
        self.assertIsNone(self.q.pop())

@unittest.skip("LifoSQLiteQueue not available in queuelib.queue")
class TestLifoSQLiteQueuePublic(unittest.TestCase):
    def setUp(self):
        self.dbfile = "test_lifo_sqlite_public.db"
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
        from queuelib.queue import LifoSQLiteQueue
        self.q = LifoSQLiteQueue("sqlite:///" + self.dbfile)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
    def test_lifo_sqlite_different(self):
        self.q.push(b"one")
        self.q.push(b"two")
        self.q.push(b"three")
        self.assertEqual(self.q.pop(), b"three")
        self.assertEqual(self.q.pop(), b"two")
        self.assertEqual(self.q.pop(), b"one")
        self.assertIsNone(self.q.pop())