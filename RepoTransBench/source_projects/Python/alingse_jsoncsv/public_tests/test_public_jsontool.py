# Public test cases for jsoncsv.jsontool with different input/data

import io
import unittest

from jsoncsv.jsontool import expand, restore
from jsoncsv.jsontool import is_array_index
from jsoncsv.jsontool import convert_json

class TestPublicJSONTool(unittest.TestCase):
    def test_string(self):
        s = "public_string"
        exp = expand(s)
        _s = restore(exp)
        self.assertEqual(s, _s)

    def test_list(self):
        s = ["alpha", "beta", 99, 42, ["public"]]
        exp = expand(s)
        _s = restore(exp)
        self.assertListEqual(s, _s)

    def test_dict(self):
        s = {
            "foo": 123,
            "bar": 321,
            "nested": {
                "sub": 10,
                "level2": {"deep": "blue"}
            },
        }
        exp = expand(s)
        _s = restore(exp)
        self.assertDictEqual(s, _s)

    def test_complex(self):
        s = [
            {"x": 100},
            {"y": ["v", {"a": "b"}]},
            7,
            "z",
            ["y", "h", 0]
        ]
        exp = expand(s)
        _s = restore(exp)
        self.assertDictEqual(s[0], _s[0])
        self.assertDictEqual(s[1], _s[1])
        self.assertEqual(s[2], _s[2])
        self.assertEqual(s[3], _s[3])
        self.assertListEqual(s[4], _s[4])

    def test_is_array_index(self):
        self.assertTrue(is_array_index([4, 2, 0, 1, 3]))
        self.assertTrue(is_array_index(['2', '1', '0']))
        self.assertTrue(is_array_index(['0', '1', '2', '11', '5', '4', '6', '7', '8', '9']))
        self.assertFalse(is_array_index([1, 3, 5]))
        self.assertFalse(is_array_index(['0', 1, '2']))

    def test_unicode(self):
        data = [
            {u"城市": u"北京", u"面积": u"16000平方千米"},
            {u"城市": u"上海", u"面积": u"6000平方千米"}
        ]
        expobj = expand(data)
        assert expobj

    def test_expand_with_safe(self):
        data = {
            "example.com": {"rt": 200, "p99": 23},
            "api.site.com": {"rt": 201, "p999": 145, "err": 9},
        }
        expobj = expand(data, safe=True)
        self.assertEqual(expobj['api.site.com\\.p999'], 145)
        self.assertEqual(expobj['api.site.com\\.err'], 9)
        origin = restore(expobj, safe=True)
        self.assertEqual(origin, data)

    def test_expand_and_restore(self):
        data = ["red", "orange", "blue"] * 3
        expobj = expand(data)
        self.assertEqual(expobj["0"], "red")
        self.assertEqual(expobj["1"], "orange")
        origin = restore(expobj)
        self.assertEqual(data, origin)


class TestPublicConvertJSON(unittest.TestCase):
    def test_convert_expand(self):
        fin = io.StringIO(u'{"x":{"y":88}}\n{"x":{"z":99}}\n')
        fout = io.StringIO()

        convert_json(fin, fout, expand)

        self.assertEqual('{"x.y": 88}\n{"x.z": 99}\n', fout.getvalue())
        fin.close()
        fout.close()

    def test_convert_with_unicode(self):
        fin = io.StringIO(u'{"国家":{"首都":1}}\n{"国家":{"人口":"11亿"}}\n')
        fout = io.StringIO()
        convert_json(fin, fout, expand)
        self.assertEqual(u'{"国家.首都": 1}\n{"国家.人口": "11亿"}\n', fout.getvalue())
        fin.close()
        fout.close()

    def test_convert_restore(self):
        fin = io.StringIO(u'{"u.v": 88}\n{"u.w": 99}\n')
        fout = io.StringIO()
        convert_json(fin, fout, restore)
        self.assertEqual('{"u": {"v": 88}}\n{"u": {"w": 99}}\n', fout.getvalue())
        fin.close()
        fout.close()

    def test_convert_expand_json_array(self):
        fin = io.StringIO(u'[{"foo":{"bar":5}},{"foo":{"baz":6}}]')
        fout = io.StringIO()
        convert_json(fin, fout, expand, json_array=True)
        self.assertEqual('{"foo.bar": 5}\n{"foo.baz": 6}\n', fout.getvalue())
        fin.close()
        fout.close()