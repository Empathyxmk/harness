import unittest
from queuelib.queue import FifoMemoryQueue, LifoMemoryQueue, BaseQueue, _BaseQueueMeta

class AnotherDummyQueue:
    def push(self, obj): pass
    def pop(self): return None
    def peek(self): return None
    def close(self): pass
    def __len__(self): return 0

class TestBaseQueueMetaPublic(unittest.TestCase):
    def test_instance_and_subclass(self):
        self.assertTrue(isinstance(AnotherDummyQueue(), BaseQueue))
        self.assertTrue(issubclass(AnotherDummyQueue, BaseQueue))
        class NonQueue: pass
        self.assertFalse(isinstance(NonQueue(), BaseQueue))
        self.assertFalse(issubclass(NonQueue, BaseQueue))

class TestFifoMemoryQueuePublic(unittest.TestCase):
    def test_fifo_alternate(self):
        q = FifoMemoryQueue()
        self.assertEqual(len(q), 0)
        q.push(100)
        q.push(200)
        q.push(300)
        self.assertEqual(len(q), 3)
        self.assertEqual(q.peek(), 100)
        self.assertEqual(q.pop(), 100)
        self.assertEqual(q.peek(), 200)
        self.assertEqual(q.pop(), 200)
        self.assertEqual(q.peek(), 300)
        self.assertEqual(q.pop(), 300)
        self.assertIsNone(q.peek())
        self.assertIsNone(q.pop())
        q.close()

    def test_empty_behaviour(self):
        q = FifoMemoryQueue()
        self.assertIsNone(q.peek())
        self.assertIsNone(q.pop())
        q.close()

class TestLifoMemoryQueuePublic(unittest.TestCase):
    def test_lifo_alternate(self):
        q = LifoMemoryQueue()
        self.assertEqual(len(q), 0)
        q.push('x')
        q.push('y')
        q.push('z')
        self.assertEqual(len(q), 3)
        self.assertEqual(q.peek(), 'z')
        self.assertEqual(q.pop(), 'z')
        self.assertEqual(q.peek(), 'y')
        self.assertEqual(q.pop(), 'y')
        self.assertEqual(q.peek(), 'x')
        self.assertEqual(q.pop(), 'x')
        self.assertIsNone(q.peek())
        self.assertIsNone(q.pop())
        q.close()

if __name__ == "__main__":
    unittest.main()