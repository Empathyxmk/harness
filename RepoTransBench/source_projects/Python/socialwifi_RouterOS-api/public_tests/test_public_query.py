from unittest import TestCase
from routeros_api import query

class TestQueryPublic(TestCase):
    def test_add_and_str(self):
        q = query.Query()
        q.add('foo', 'bar')
        q.add('baz', 'qux')
        self.assertEqual(str(q), "Query(foo='bar', baz='qux')")

    def test_reset_and_len(self):
        q = query.Query()
        q.add('a', 1)
        q.add('b', 2)
        self.assertEqual(len(q), 2)
        q.reset()
        self.assertEqual(len(q), 0)