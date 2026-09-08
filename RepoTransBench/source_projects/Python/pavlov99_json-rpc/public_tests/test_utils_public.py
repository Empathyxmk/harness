from jsonrpc.utils import JSONSerializable, DatetimeDecimalEncoder, is_invalid_params
import datetime
import decimal
import json
import sys
import unittest

if sys.version_info < (3, 3):
    from mock import patch
else:
    from unittest.mock import patch


class TestJSONSerializablePublic(unittest.TestCase):

    def setUp(self):
        class B(JSONSerializable):
            @property
            def json(self):
                pass

        self._class = B

    def test_abstract_class(self):
        with self.assertRaises(TypeError):
            JSONSerializable()

        self._class()

    def test_definse_serialize_deserialize(self):
        self.assertEqual(self._class.serialize({"key": 111}), '{"key": 111}')
        self.assertEqual(self._class.deserialize('{"foo": "bar"}'), {"foo": "bar"})

    def test_from_json(self):
        instance = self._class.from_json('{"hello": "world"}')
        self.assertTrue(isinstance(instance, self._class))

    def test_from_json_incorrect(self):
        with self.assertRaises(ValueError):
            self._class.from_json('"not a dict"')


class TestDatetimeDecimalEncoderPublic(unittest.TestCase):

    def test_date_encoder(self):
        obj = datetime.date(2000, 1, 1)

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"2000-01-01"',
        )

    def test_datetime_encoder(self):
        obj = datetime.datetime(2015, 5, 6, 7, 8, 9)

        with self.assertRaises(TypeError):
            json.dumps(obj)

        self.assertEqual(
            json.dumps(obj, cls=DatetimeDecimalEncoder),
            '"2015-05-06T07:08:09"',
        )

    def test_decimal_encoder(self):
        obj = decimal.Decimal('2.5')
        with self.assertRaises(TypeError):
            json.dumps(obj)

        result = json.dumps(obj, cls=DatetimeDecimalEncoder)
        self.assertTrue(isinstance(result, str))
        self.assertEqual(float(result), float(2.5))

    def test_default(self):
        encoder = DatetimeDecimalEncoder()
        with patch.object(json.JSONEncoder, 'default') as json_default:
            encoder.default(999)
        self.assertEqual(json_default.call_count, 1)


class TestUtilsPublic(unittest.TestCase):

    def test_is_invalid_params_builtin(self):
        self.assertTrue(is_invalid_params(pow, 2))
        # NOTE: builtin functions could not be recognized by inspect.isfunction
        # It would raise TypeError if parameters are incorrect already.

    def test_is_invalid_params_args(self):
        self.assertTrue(is_invalid_params(lambda x, y: None, 1))
        self.assertTrue(is_invalid_params(lambda x, y: None, 1, 2, 3))

    def test_is_invalid_params_kwargs(self):
        self.assertTrue(is_invalid_params(lambda d: None, **{}))
        self.assertTrue(is_invalid_params(lambda d: None, **{"d": 1, "e": 2}))

    def test_invalid_params_correct(self):
        self.assertFalse(is_invalid_params(lambda: None))
        self.assertFalse(is_invalid_params(lambda x: None, 33))
        self.assertFalse(is_invalid_params(lambda x, y=3: None, 11))
        self.assertFalse(is_invalid_params(lambda x, y=3: None, 64, 39))

    def test_is_invalid_params_mixed(self):
        self.assertFalse(is_invalid_params(lambda x, y: None, 5, **{"y": 12}))
        self.assertFalse(is_invalid_params(
            lambda a, b, c=0: None, 8, **{"b": 9}))

    def test_is_invalid_params_py2(self):
        with patch('jsonrpc.utils.sys') as mock_sys:
            mock_sys.version_info = (2, 7)
            with patch('jsonrpc.utils.is_invalid_params_py2') as mock_func:
                is_invalid_params(lambda a: None, 0)
        assert mock_func.call_count == 1