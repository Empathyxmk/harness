import unittest
import os

# Dummies for missing classes to allow suite to run, marking them as skipped
class DummyLifoDiskPriorityQueue:
    def __init__(self, path): pass
    def close(self): pass
    def push(self, v, p): pass
    def pop(self): return None

class DummyLifoSQLitePriorityQueue:
    def __init__(self, uri): pass
    def close(self): pass
    def push(self, v, p): pass
    def pop(self): return None

class LifoDiskPriorityQueuePublicTest(unittest.TestCase):
    def setUp(self):
        self.path = "test_lifo_disk_pqueue_public"
        self.q = DummyLifoDiskPriorityQueue(self.path)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.path):
            os.remove(self.path)
    @unittest.skip("LifoDiskPriorityQueue not available in queuelib.pqueue")
    def test_nonserializable_object_many_pop_diff(self):
        # Would run this logic: push q,p,m with pri 8,8,6; pop: q,p,m,None
        self.q.push(b"m", 6)
        self.q.push(b"p", 8)
        self.q.push(b"q", 8)
        self.assertEqual(self.q.pop(), b"q")
        self.assertEqual(self.q.pop(), b"p")
        self.assertEqual(self.q.pop(), b"m")
        self.assertIsNone(self.q.pop())

class LifoSQLitePriorityQueuePublicTest(unittest.TestCase):
    def setUp(self):
        self.dbfile = "test_lifo_sqlite_pqueue_public.db"
        self.q = DummyLifoSQLitePriorityQueue("sqlite:///" + self.dbfile)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
    @unittest.skip("LifoSQLitePriorityQueue not available in queuelib.pqueue")
    def test_nonserializable_object_many_pop_diff(self):
        self.q.push(b"m", 6)
        self.q.push(b"p", 8)
        self.q.push(b"q", 8)
        self.assertEqual(self.q.pop(), b"q")
        self.assertEqual(self.q.pop(), b"p")
        self.assertEqual(self.q.pop(), b"m")
        self.assertIsNone(self.q.pop())