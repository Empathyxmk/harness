import unittest
from queuelib.queue import FifoMemoryQueue, LifoMemoryQueue, BaseQueue, _BaseQueueMeta


class DummyQueue:
    def push(self, obj): pass
    def pop(self): return None
    def peek(self): return None
    def close(self): pass
    def __len__(self): return 0


class TestBaseQueueMeta(unittest.TestCase):
    def test_instancecheck_and_subclasscheck(self):
        # Should recognize correct interface
        self.assertTrue(isinstance(DummyQueue(), BaseQueue))
        self.assertTrue(issubclass(DummyQueue, BaseQueue))
        class NotAQueue: pass
        self.assertFalse(isinstance(NotAQueue(), BaseQueue))
        self.assertFalse(issubclass(NotAQueue, BaseQueue))

class TestFifoMemoryQueue(unittest.TestCase):
    def test_fifo_normal(self):
        q = FifoMemoryQueue()
        self.assertEqual(len(q), 0)
        q.push(1)
        q.push(2)
        self.assertEqual(len(q), 2)
        self.assertEqual(q.peek(), 1)
        self.assertEqual(q.pop(), 1)
        self.assertEqual(q.peek(), 2)
        self.assertEqual(q.pop(), 2)
        self.assertIsNone(q.peek())
        self.assertIsNone(q.pop())
        q.close()

    def test_empty_pop_peek(self):
        q = FifoMemoryQueue()
        self.assertIsNone(q.pop())
        self.assertIsNone(q.peek())
        q.close()

class TestLifoMemoryQueue(unittest.TestCase):
    def test_lifo_normal(self):
        q = LifoMemoryQueue()
        self.assertEqual(len(q), 0)
        q.push('a')
        q.push('b')
        self.assertEqual(len(q), 2)
        self.assertEqual(q.peek(), 'b')
        self.assertEqual(q.pop(), 'b')
        self.assertEqual(q.peek(), 'a')
        self.assertEqual(q.pop(), 'a')
        self.assertIsNone(q.peek())
        self.assertIsNone(q.pop())
        q.close()


if __name__ == "__main__":
    unittest.main()