import json
import unittest

from jsonrpc.jsonrpc2 import (
    JSONRPC20Request,
    JSONRPC20Response,
    JSONRPC20BatchRequest,
    JSONRPC20BatchResponse,
)


class TestJSONRPC20RequestPublic(unittest.TestCase):

    def test_valid_request_object(self):
        req = JSONRPC20Request(method="publicMethod2", params=[88, 22], _id=99)
        self.assertEqual(req.data["method"], "publicMethod2")
        self.assertEqual(req.data["params"], [88, 22])
        self.assertEqual(req.data["id"], 99)
        self.assertEqual(req.data["jsonrpc"], "2.0")

    def test_notification(self):
        req = JSONRPC20Request(method="eventNotify", params=[42], _id=None, is_notification=True)
        data = req.data
        self.assertEqual(data["method"], "eventNotify")
        self.assertEqual(data["params"], [42])
        self.assertTrue("id" not in data)
        self.assertEqual(data["jsonrpc"], "2.0")

    def test_params_types_list_and_dict(self):
        req = JSONRPC20Request(method="f2", params=[13, 21], _id=2)
        self.assertEqual(req.data["params"], [13, 21])
        req2 = JSONRPC20Request(method="f3", params={"key": 51, "val": 999}, _id="Gamma")
        self.assertEqual(req2.data["params"], {"key": 51, "val": 999})

    def test_params_none_is_ok(self):
        # Accepts params=None as per code, just omits the params field, so should not raise
        req = JSONRPC20Request(method="has_none_params", params=None, _id=1)
        self.assertTrue(isinstance(req, JSONRPC20Request))

    def test_params_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="wrongtype", params="notalistordict", _id="a")
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="wrongtype", params=21, _id="w")
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="wrongtype", params=42.13, _id="z")
    
    def test_method_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC20Request(method=333, params=[], _id=None)
        with self.assertRaises(ValueError):
            JSONRPC20Request(method=["m2"], params=[], _id=None)

    def test_id_types(self):
        JSONRPC20Request(method="fooPublic", params=[10], _id="alfa")
        JSONRPC20Request(method="fooPublic", params=[322], _id=99)
        JSONRPC20Request(method="fooPublic", params=[1], _id=None)
        # Verify id rejects non-str/non-int
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="fooPublic", params=[42], _id=5.55)
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="fooPublic", params=[23], _id=["not", "id"])
        with self.assertRaises(ValueError):
            JSONRPC20Request(method="fooPublic", params=[17], _id=("tuple",))

    def test_json_output(self):
        req = JSONRPC20Request("sumFun", params=[9, 101], _id=101)
        parsed = json.loads(req.json)
        self.assertEqual(parsed, req.data)
        self.assertEqual(parsed["method"], "sumFun")
        self.assertEqual(parsed["params"], [9, 101])
        self.assertEqual(parsed["id"], 101)
        self.assertEqual(parsed["jsonrpc"], "2.0")

    def test_notification_id(self):
        req = JSONRPC20Request("logevt", params=[], _id="should_be_ignored", is_notification=True)
        self.assertTrue("id" not in req.data)

    def test_args(self):
        self.assertEqual(JSONRPC20Request("multi", [7, 5]).args, (7, 5))
        self.assertEqual(JSONRPC20Request("named", {"x": 1000, "y": 47}).args, ())


class TestJSONRPC20ResponsePublic(unittest.TestCase):

    def test_valid_response(self):
        JSONRPC20Response(result="done", error=None, _id=88)
        # error must be a dict or None, so this should raise
        with self.assertRaises(TypeError):
            JSONRPC20Response(result=None, error="failReason", _id="badid2")
        err_dict = dict(code=7, message="Error7")
        JSONRPC20Response(result=None, error=err_dict, _id="errtest200")

    def test_json_output(self):
        resp = JSONRPC20Response(result="result_val", error=None, _id=123)
        parsed = json.loads(resp.json)
        self.assertEqual(parsed, resp.data)
        self.assertEqual(parsed["result"], "result_val")
        self.assertNotIn("error", parsed)
        self.assertEqual(parsed["id"], 123)
        self.assertEqual(parsed["jsonrpc"], "2.0")

        err_d = {"code": 1001, "message": "Fail error"}
        resp = JSONRPC20Response(result=None, error=err_d, _id="failid")
        parsed = json.loads(resp.json)
        self.assertEqual(parsed["result"], None)
        self.assertEqual(parsed["error"], err_d)
        self.assertEqual(parsed["id"], "failid")
        self.assertEqual(parsed["jsonrpc"], "2.0")

    def test_init_invalid(self):
        with self.assertRaises(TypeError):
            JSONRPC20Response()


class TestJSONRPC20BatchRequestPublic(unittest.TestCase):
    def test_batch_request(self):
        items = [
            JSONRPC20Request("applep", params=[11, 32], _id=1401),
            JSONRPC20Request("bananap", params={"x": 45}, _id="str901"),
            JSONRPC20Request("cucumberp", params=[], _id=None),
        ]
        batch = JSONRPC20BatchRequest(items)
        data = batch.data
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["method"], "applep")
        self.assertEqual(data[1]["method"], "bananap")
        self.assertEqual(data[2]["method"], "cucumberp")

    def test_batch_request_json(self):
        items = [
            JSONRPC20Request("funkey", [99], _id="sid1337"),
            JSONRPC20Request("bazbaz", [], _id=None),
        ]
        batch = JSONRPC20BatchRequest(items)
        self.assertEqual(json.loads(batch.json), batch.data)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC20BatchRequest(["not_a_request", "object"])
        with self.assertRaises(ValueError):
            JSONRPC20BatchRequest(JSONRPC20Request("should_fail", [12]))

class TestJSONRPC20BatchResponsePublic(unittest.TestCase):
    def test_batch_response(self):
        items = [
            JSONRPC20Response(result="tangerine", error=None, _id=134),
            JSONRPC20Response(result=None, error={"code": 4, "message": "peach"}, _id="id1313"),
        ]
        batch = JSONRPC20BatchResponse(items)
        data = batch.data
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["result"], "tangerine")
        self.assertEqual(data[1]["error"], {"code": 4, "message": "peach"})

    def test_batch_response_json(self):
        items = [
            JSONRPC20Response(result="fooout", error=None, _id="h321"),
            JSONRPC20Response(result=None, error={"code": 88, "message": "errormsg"}, _id=None),
        ]
        batch = JSONRPC20BatchResponse(items)
        self.assertEqual(json.loads(batch.json), batch.data)

    def test_invalid_type(self):
        with self.assertRaises(ValueError):
            JSONRPC20BatchResponse(["not_a_response", "object"])
        with self.assertRaises(ValueError):
            JSONRPC20BatchResponse(JSONRPC20Response(result="fail_batch", error=None, _id=42))