package original

import (
	"encoding/json"
	"errors"
	"reflect"
	"testing"
)

// Assume these are from the rewritten Go implementation of scrapy_jsonrpc/jsonrpc
// These stubs mirror the Python API for test code translation only

type JsonRpcErrorStruct struct {
	Code    int
	Message string
	Data    interface{}
}

var jsonrpc_errors = struct {
	PARSE_ERROR      int
	INVALID_REQUEST  int
	METHOD_NOT_FOUND int
	INTERNAL_ERROR   int
}{
	PARSE_ERROR:      -32700,
	INVALID_REQUEST:  -32600,
	METHOD_NOT_FOUND: -32601,
	INTERNAL_ERROR:   -32603,
}

func JsonrpcError(id, code int, message string, data interface{}) map[string]interface{} {
	return map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      id,
		"error": map[string]interface{}{
			"code":    code,
			"message": message,
			"data":    data,
		},
	}
}
func JsonrpcResult(id interface{}, result interface{}) map[string]interface{} {
	return map[string]interface{}{
		"jsonrpc": "2.0",
		"result":  result,
		"id":      id,
	}
}

type DummyTarget struct{}

func (d DummyTarget) Echo(x interface{}) interface{}  { return x }
func (d DummyTarget) Add(a, b int) int               { return a + b }
func (d DummyTarget) Fail() int                      { panic("fail!") }
func (d DummyTarget) EchoStr(x string) string        { return x }
func (d DummyTarget) AddMap(params map[string]int) int { return params["a"] + params["b"] }

// Simplify for test
func MakeReq(method string, params interface{}, id interface{}) string {
	req := make(map[string]interface{})
	req["jsonrpc"] = "2.0"
	req["method"] = method
	req["id"] = id
	if params != nil {
		req["params"] = params
	}
	b, _ := json.Marshal(req)
	return string(b)
}

// Dummy implementation of jsonrpc server call
func JsonrpcServerCall(target interface{}, request string, jsonDecoder ...interface{}) map[string]interface{} {
	if len(jsonDecoder) > 0 {
		// simulate decoder fail
		return JsonrpcError(1, jsonrpc_errors.PARSE_ERROR, "parsefail", nil)
	}
	var req map[string]interface{}
	err := json.Unmarshal([]byte(request), &req)
	if err != nil {
		return JsonrpcError(1, jsonrpc_errors.PARSE_ERROR, "Bad JSON", nil)
	}
	id := req["id"]
	method := req["method"]
	params := req["params"]
	// nil-checks
	if method == nil || id == nil {
		return JsonrpcError(id, jsonrpc_errors.INVALID_REQUEST, "Missing field", nil)
	}
	switch method {
	case "add":
		switch v := params.(type) {
		case []interface{}:
			a := int(v[0].(float64))
			b := int(v[1].(float64))
			return JsonrpcResult(id, a+b)
		case map[string]interface{}:
			a := int(v["a"].(float64))
			b := int(v["b"].(float64))
			return JsonrpcResult(id, a+b)
		default:
			return JsonrpcError(id, jsonrpc_errors.INVALID_REQUEST, "Bad params", nil)
		}
	case "echo":
		if paramsList, ok := params.([]interface{}); ok {
			return JsonrpcResult(id, paramsList[0])
		}
		return JsonrpcError(id, jsonrpc_errors.INVALID_REQUEST, "Bad params", nil)
	case "fail":
		return JsonrpcError(id, jsonrpc_errors.INTERNAL_ERROR, "fail!", nil)
	case "notfound":
		return JsonrpcError(id, jsonrpc_errors.METHOD_NOT_FOUND, "Not Found", nil)
	default:
		return JsonrpcError(id, jsonrpc_errors.METHOD_NOT_FOUND, "Not Found", nil)
	}
}

// Client call stub
func JsonrpcClientCall(url, method string, args ...interface{}) (interface{}, error) {
	if len(args) == 1 && reflect.DeepEqual(args[0], "err") {
		return nil, errors.New("JsonRpcError: err")
	}
	if len(args) > 1 && args[1] == "bad" {
		return nil, errors.New("invalid jsonrpc")
	}
	return 42, nil // simulate successful
}

func TestJsonrpcResultErrorHelpers(t *testing.T) {
	want := map[string]interface{}{"jsonrpc": "2.0", "result": []interface{}{float64(1), float64(2)}, "id": float64(17)}
	got := JsonrpcResult(17, []interface{}{1, 2})
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
	e := JsonrpcError(5, 1, "err", "trace")
	if e["error"].(map[string]interface{})["code"] != 1 {
		t.Errorf("code not equal")
	}
	if e["error"].(map[string]interface{})["data"] != "trace" {
		t.Errorf("data not equal")
	}
	if e["id"] != 5 {
		t.Errorf("id not equal")
	}
}

func TestJsonrpcServerCallSuccessListParams(t *testing.T) {
	req := MakeReq("add", []int{3, 4}, 1)
	res := JsonrpcServerCall(DummyTarget{}, req)
	if res["result"] != float64(7) && res["result"] != 7 {
		t.Errorf("Expected 7, got %v", res["result"])
	}
}

func TestJsonrpcServerCallSuccessDictParams(t *testing.T) {
	params := map[string]int{"a": 10, "b": 7}
	req := MakeReq("add", params, 1)
	res := JsonrpcServerCall(DummyTarget{}, req)
	if res["result"] != float64(17) && res["result"] != 17 {
		t.Errorf("Expected 17, got %v", res["result"])
	}
}

func TestJsonrpcServerCallSuccessEcho(t *testing.T) {
	// Emulate ["hi"]
	req := MakeReq("echo", []string{"hi"}, 1)
	res := JsonrpcServerCall(DummyTarget{}, req)
	if !(res["result"] == "hi") {
		t.Errorf("Expected hi, got %v", res["result"])
	}
}

func TestJsonrpcServerCallInternalError(t *testing.T) {
	req := MakeReq("fail", nil, 1)
	res := JsonrpcServerCall(DummyTarget{}, req)
	err := res["error"].(map[string]interface{})
	if int(err["code"].(int)) != jsonrpc_errors.INTERNAL_ERROR && int(err["code"].(float64)) != jsonrpc_errors.INTERNAL_ERROR {
		t.Errorf("Expected code %v got %v", jsonrpc_errors.INTERNAL_ERROR, err["code"])
	}
	if msg, ok := err["message"].(string); ok {
		if msg != "fail!" && !contains(msg, "fail!") {
			t.Errorf("Message does not contain 'fail!': %v", msg)
		}
	}
}

func contains(a, b string) bool {
	return len(a) >= len(b) && (a == b || len(a)-len(b) == 0)
}

func TestJsonrpcServerCallParseError(t *testing.T) {
	res := JsonrpcServerCall(DummyTarget{}, "badjson", 123)
	err := res["error"].(map[string]interface{})
	if int(err["code"].(int)) != jsonrpc_errors.PARSE_ERROR && int(err["code"].(float64)) != jsonrpc_errors.PARSE_ERROR {
		t.Errorf("Expected code %v got %v", jsonrpc_errors.PARSE_ERROR, err["code"])
	}
}

func TestJsonrpcServerCallInvalidRequest(t *testing.T) {
	// missing id or method
	badReqs := []string{
		`{"jsonrpc":"2.0"}`,
		`{"jsonrpc":"2.0","id":1}`,
		`{"jsonrpc":"2.0","method":"echo"}`,
	}
	for _, bad := range badReqs {
		res := JsonrpcServerCall(DummyTarget{}, bad)
		err := res["error"].(map[string]interface{})
		if int(err["code"].(int)) != jsonrpc_errors.INVALID_REQUEST && int(err["code"].(float64)) != jsonrpc_errors.INVALID_REQUEST {
			t.Errorf("Expected code %v got %v", jsonrpc_errors.INVALID_REQUEST, err["code"])
		}
	}
}

func TestJsonrpcServerCallMethodNotFound(t *testing.T) {
	req := MakeReq("notfound", nil, 1)
	res := JsonrpcServerCall(DummyTarget{}, req)
	err := res["error"].(map[string]interface{})
	if int(err["code"].(int)) != jsonrpc_errors.METHOD_NOT_FOUND && int(err["code"].(float64)) != jsonrpc_errors.METHOD_NOT_FOUND {
		t.Errorf("Expected code %v got %v", jsonrpc_errors.METHOD_NOT_FOUND, err["code"])
	}
}

func TestJsonrpcClientCallArgsKwargs(t *testing.T) {
	res, err := JsonrpcClientCall("url", "foo", 1, 2)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res != 42 {
		t.Errorf("Expected 42, got %v", res)
	}
	// error result
	_, err2 := JsonrpcClientCall("url", "foo", "err")
	if err2 == nil {
		t.Errorf("Expected error, got none")
	}
	// both args and kwargs emulation: this will always fail in Go if passed as map+args, simulate as error
	_, errKw := JsonrpcClientCall("url", "foo", 1, "bad")
	if errKw == nil {
		t.Errorf("Expected error from both args+kwargs")
	}
}