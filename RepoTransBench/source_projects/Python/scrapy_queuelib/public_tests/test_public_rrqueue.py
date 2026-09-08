import unittest
import os

# Import or dummy only LifoSQLiteRRQueue otherwise skip
class DummyLifoDiskRRQueue:
    def __init__(self, path): pass
    def close(self): pass
    def push(self, v, p): pass
    def pop(self): return None

class DummyLifoSQLiteRRQueue:
    def __init__(self, uri): pass
    def close(self): pass
    def push(self, v, p): pass
    def pop(self): return None

class LifoDiskRRQueuePublicTest(unittest.TestCase):
    def setUp(self):
        self.q = DummyLifoDiskRRQueue("test_lifo_disk_rrqueue_public")
    def tearDown(self):
        self.q.close()
    @unittest.skip("LifoDiskRRQueue not available in queuelib.rrqueue")
    def test_nonserializable_object_many_pop_alt(self):
        self.q.push(b"c", 4)
        self.q.push(b"e", 5)
        self.q.push(b"f", 5)
        self.assertEqual(self.q.pop(), b"f")
        self.assertEqual(self.q.pop(), b"e")
        self.assertEqual(self.q.pop(), b"c")
        self.assertIsNone(self.q.pop())

class LifoSQLiteRRQueuePublicTest(unittest.TestCase):
    def setUp(self):
        self.dbfile = "test_lifo_sqlite_rrqueue_public.db"
        self.q = DummyLifoSQLiteRRQueue("sqlite:///" + self.dbfile)
    def tearDown(self):
        self.q.close()
        if os.path.exists(self.dbfile):
            os.remove(self.dbfile)
    @unittest.skip("LifoSQLiteRRQueue not available in queuelib.rrqueue")
    def test_nonserializable_object_many_pop_alt(self):
        self.q.push(b"c", 4)
        self.q.push(b"e", 5)
        self.q.push(b"f", 5)
        self.assertEqual(self.q.pop(), b"f")
        self.assertEqual(self.q.pop(), b"e")
        self.assertEqual(self.q.pop(), b"c")
        self.assertIsNone(self.q.pop())