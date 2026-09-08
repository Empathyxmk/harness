import unittest
import os
import tempfile
import types
import sqlitedict
from sqlitedict import encode, decode, encode_key, decode_key, identity, reraise

class TestUtilsAndHelpers(unittest.TestCase):

    def test_encode_decode(self):
        d = {"a": 1, "b": 2}
        b = encode(d)
        self.assertEqual(decode(b), d)

    def test_encode_decode_key(self):
        k = "mykey"
        k_encoded = encode_key(k)
        self.assertEqual(decode_key(k_encoded), k)

    def test_identity(self):
        val = object()
        self.assertIs(identity(val), val)

    def test_reraise(self):
        try:
            try:
                raise ValueError("boo")
            except Exception as e:
                _, _, tb = e.__class__, e, e.__traceback__
                reraise(ValueError, e, tb)
        except ValueError as e2:
            self.assertEqual(str(e2), "boo")
    
    def test_open_function(self):
        tmp = tempfile.mktemp()
        d = sqlitedict.open(tmp)
        d['x'] = 12
        self.assertEqual(d['x'], 12)
        d.close()
        os.remove(tmp)

class TestPutFunction(unittest.TestCase):
    def test_put_variants(self):
        from sqlitedict import _put, _PUT_OK, _PUT_REFERENT_DESTROYED, _PUT_NOOP
        class DummyQueue:
            def __init__(self):
                self.vals = []
                self.destroyed = False
            def put(self, v):
                if self.destroyed:
                    raise ReferenceError
                self.vals.append(v)
        q = DummyQueue()
        import weakref
        ref = weakref.ref(q)
        self.assertEqual(_put(ref, "item"), _PUT_OK)
        # simulate destruction
        q.destroyed = True
        del q
        import gc; gc.collect()
        self.assertIn(_put(ref, "item2"), [_PUT_REFERENT_DESTROYED, _PUT_OK])

    def test_put_noop(self):
        from sqlitedict import _put, _PUT_NOOP
        self.assertEqual(_put(None, "hi"), _PUT_NOOP)

if __name__ == '__main__':
    unittest.main()