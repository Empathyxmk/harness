import json
import unittest

from jsonrpc.jsonrpc1 import (
    JSONRPC10Request,
    JSONRPC10Response,
    JSONRPC10BatchRequest,
    JSONRPC10BatchResponse,
)

class TestJSONRPC10RequestPublic(unittest.TestCase):

    def test_valid_request_object(self):
        req = JSONRPC10Request(method="add_public", params=[56, 34], _id=101)
        self.assertEqual(req.data["method"], "add_public")
        self.assertEqual(req.data["params"], [56, 34])
        self.assertEqual(req.data["id"], 101)

    def test_params_types_list_and_dict(self):
        req = JSONRPC10Request(method="echo_public", params=[1, "bar"], _id=202)
        self.assertEqual(req.data["params"], [1, "bar"])
        req2 = JSONRPC10Request(method="echo_dict_public", params={"foo_bar": 18}, _id="id_a")
        self.assertEqual(req2.data["params"], {"foo_bar": 18})

    def test_params_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="fail_param", params="hello", _id=1)
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="fail_param", params=99, _id=1)
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="fail_param", params=7.14, _id=1)

    def test_method_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC10Request(method=444, params=[], _id=None)
        with self.assertRaises(ValueError):
            JSONRPC10Request(method=["pub"], params=[], _id=None)

    def test_id_types(self):
        JSONRPC10Request(method="has_id", params=[33], _id="foobar")
        JSONRPC10Request(method="has_id", params=[11], _id=222)
        JSONRPC10Request(method="has_id", params=[0], _id=None)
        # Verify id rejects non-str/non-int
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="badid", params=[12], _id=4.5)
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="badid", params=[23], _id=["bad"])
        with self.assertRaises(ValueError):
            JSONRPC10Request(method="badid", params=[29], _id=("t",))

    def test_json_output(self):
        req = JSONRPC10Request("multiply_public", params=[5, 8], _id=120)
        parsed = json.loads(req.json)
        self.assertEqual(parsed, req.data)
        self.assertEqual(parsed["method"], "multiply_public")
        self.assertEqual(parsed["params"], [5, 8])
        self.assertEqual(parsed["id"], 120)

    def test_args(self):
        self.assertEqual(JSONRPC10Request("multi_pub", [12, 4]).args, (12, 4))
        self.assertEqual(JSONRPC10Request("named_pub", {"x": 87, "y": 21}).args, ())

class TestJSONRPC10ResponsePublic(unittest.TestCase):

    def test_valid_response(self):
        JSONRPC10Response(result="pass", error=None, _id=98)
        # error must be a dict or None, so this should raise
        with self.assertRaises(TypeError):
            JSONRPC10Response(result=None, error="fail", _id="errID")
        err_dict = dict(code=404, message="NF")
        JSONRPC10Response(result=None, error=err_dict, _id="errdictid")

    def test_to_json(self):
        rsp = JSONRPC10Response(result="hi", error=None, _id=34)
        self.assertEqual(json.loads(rsp.json), rsp.data)
        self.assertEqual(rsp.data["result"], "hi")
        self.assertNotIn("error", rsp.data)
        self.assertEqual(rsp.data["id"], 34)

        err_dict = {"code": 12, "message": "Crash"}
        rsp = JSONRPC10Response(result=None, error=err_dict, _id="cc10")
        data = json.loads(rsp.json)
        self.assertEqual(data["error"], err_dict)
        self.assertEqual(data["id"], "cc10")

    def test_init(self):
        JSONRPC10Response(result="foo", error=None, _id=44)
        # next should raise TypeError (error must be dict/None)
        with self.assertRaises(TypeError):
            JSONRPC10Response(result=None, error="fail", _id="erridpub")
        err_obj = dict(code=-777, message="allbad")
        JSONRPC10Response(result=None, error=err_obj, _id="dictidpub")

class TestJSONRPC10BatchRequestPublic(unittest.TestCase):
    def test_batch_request(self):
        items = [
            JSONRPC10Request("alfa_pub", params=[1, 3], _id=3301),
            JSONRPC10Request("beta_pub", params={"x": 82}, _id="stralpha"),
            JSONRPC10Request("zeta_pub", params=[], _id=None),
        ]
        batch = JSONRPC10BatchRequest(items)
        data = batch.data
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["method"], "alfa_pub")
        self.assertEqual(data[1]["method"], "beta_pub")
        self.assertEqual(data[2]["method"], "zeta_pub")

    def test_batch_request_json(self):
        items = [
            JSONRPC10Request("fooish_pub", [200], _id="sid9"),
            JSONRPC10Request("baz_pub", [], _id=None),
        ]
        batch = JSONRPC10BatchRequest(items)
        self.assertEqual(json.loads(batch.json), batch.data)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC10BatchRequest(["not_a_request", "object"])
        with self.assertRaises(ValueError):
            JSONRPC10BatchRequest(JSONRPC10Request("should_fail_pub", [21]))

class TestJSONRPC10BatchResponsePublic(unittest.TestCase):
    def test_batch_response(self):
        items = [
            JSONRPC10Response(result="grape", error=None, _id=444),
            JSONRPC10Response(result=None, error={"code": 2, "message": "errorB"}, _id="beta100"),
        ]
        batch = JSONRPC10BatchResponse(items)
        data = batch.data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["result"], "grape")
        self.assertEqual(data[1]["error"], {"code": 2, "message": "errorB"})

    def test_batch_response_json(self):
        items = [
            JSONRPC10Response(result="bartest", error=None, _id="h42"),
            JSONRPC10Response(result=None, error={"code": 13, "message": "wow"}, _id=None),
        ]
        batch = JSONRPC10BatchResponse(items)
        self.assertEqual(json.loads(batch.json), batch.data)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC10BatchResponse(["not_a_response", "object"])
        with self.assertRaises(ValueError):
            JSONRPC10BatchResponse(JSONRPC10Response(result="badary", error=None, _id=333))