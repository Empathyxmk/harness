# Public test cases for jsoncsv.utils encode/decode with different data

import unittest

from jsoncsv.utils import encode_safe_key, decode_safe_key

class TestPublicEscape(unittest.TestCase):
    def test_all(self):
        path = ['A1', 'B1', '..2', '\\.\\oo']
        for sep in 'REP':
            key = encode_safe_key(path, sep)
            _path = decode_safe_key(key, sep)
        self.assertListEqual(path, _path)

    def test_encode(self):
        path = ['D', 'E', 'F', 'my.site.com']
        sep = '.'
        key = encode_safe_key(path, sep)
        self.assertEqual(key, 'D\\.E\\.F\\.my.site.com')

    def test_decode(self):
        key = 'X\\.Y\\.Z\\.abc.def.com'
        sep = '.'
        path = decode_safe_key(key, sep)
        self.assertEqual(path[0], 'X')
        self.assertEqual(path[1], 'Y')
        self.assertEqual(path[2], 'Z')
        self.assertEqual(path[3], 'abc.def.com')