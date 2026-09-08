import unittest
import json

class GsonUtil:
    @staticmethod
    def parseMapToJson(map_arg):
        return json.dumps(map_arg) if map_arg is not None else "null"

    @staticmethod
    def parseJsonToBean(json_str, bean_type):
        if not json_str:
            return None
        try:
            dct = json.loads(json_str)
            return bean_type(**dct) if isinstance(dct, dict) else None
        except Exception:
            return None

    @staticmethod
    def parseJsonToMap(json_str):
        try:
            return json.loads(json_str)
        except Exception:
            return None

    @staticmethod
    def parseJsonToList(json_str, bean_type):
        try:
            lst = json.loads(json_str)
            return [bean_type(**el) for el in lst]
        except Exception:
            raise

    @staticmethod
    def getFieldValue(json_str, key):
        try:
            dct = json.loads(json_str)
            return dct.get(key, "") if isinstance(dct, dict) else None
        except Exception:
            return None

class TestBean:
    def __init__(self, name="", age=0):
        self.name = name
        self.age = age

class TestGsonUtil(unittest.TestCase):

    def test_parse_map_to_json_valid_map(self):
        data = {"foo":"bar"}
        json_str = GsonUtil.parseMapToJson(data)
        self.assertIn('"foo":"bar"', json_str)

    def test_parse_map_to_json_null_map(self):
        json_str = GsonUtil.parseMapToJson(None)
        self.assertEqual("null", json_str)

    def test_parse_json_to_bean_valid_json(self):
        json_str = '{"name":"Alice", "age":30}'
        bean = GsonUtil.parseJsonToBean(json_str, TestBean)
        self.assertIsNotNone(bean)
        self.assertEqual("Alice", bean.name)
        self.assertEqual(30, bean.age)

    def test_parse_json_to_bean_invalid_json(self):
        json_str = '{name:Alice, age:30}'
        bean = GsonUtil.parseJsonToBean(json_str, TestBean)
        self.assertIsNone(bean)

    def test_parse_json_to_map_valid_json(self):
        json_str = '{"foo":"bar","num":42}'
        parsed = GsonUtil.parseJsonToMap(json_str)
        self.assertEqual(parsed["foo"], "bar")
        self.assertEqual(parsed["num"], 42)

    def test_parse_json_to_map_invalid_json(self):
        json_str = '{foo:bar,num:42}'
        parsed = GsonUtil.parseJsonToMap(json_str)
        self.assertIsNone(parsed)

    def test_parse_json_to_list_valid(self):
        json_str = '[{"name":"A","age":1},{"name":"B","age":2}]'
        result = GsonUtil.parseJsonToList(json_str, TestBean)
        self.assertEqual(2, len(result))
        self.assertEqual("A", result[0].name)
        self.assertEqual(1, result[0].age)

    def test_parse_json_to_list_invalid(self):
        json_str = '[{name:A,age:1},{name:B,age:2}]'
        with self.assertRaises(Exception):
            GsonUtil.parseJsonToList(json_str, TestBean)

    def test_get_field_value_valid(self):
        j = '{"key":"value","other":"x"}'
        self.assertEqual("value", GsonUtil.getFieldValue(j, "key"))

    def test_get_field_value_key_not_present(self):
        j = '{"key1":"value1"}'
        self.assertEqual("", GsonUtil.getFieldValue(j, "missing"))

    def test_get_field_value_empty_json(self):
        self.assertIsNone(GsonUtil.getFieldValue("", "foo"))

    def test_get_field_value_invalid_json(self):
        j = '{key:value}'
        self.assertIsNone(GsonUtil.getFieldValue(j, "key"))