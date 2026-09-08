use scrapy_jsonrpc::jsonrpc::{JsonRpcError, jsonrpc_errors, jsonrpc_server_call, jsonrpc_error, jsonrpc_result, JsonRpcTarget, JsonDecoder};
use serde_json::{json, Value};

struct DummyTarget;

impl JsonRpcTarget for DummyTarget {
    fn call_method(&self, method: &str, params: Option<&Value>) -> Result<Value, JsonRpcError> {
        match method {
            "echo" => {
                if let Some(Value::Array(arr)) = params {
                    if arr.len() == 1 {
                        Ok(arr[0].clone())
                    } else {
                        Err(JsonRpcError { code: jsonrpc_errors::INVALID_PARAMS, message: "Invalid params".to_string(), data: None })
                    }
                } else {
                    Err(JsonRpcError { code: jsonrpc_errors::INVALID_PARAMS, message: "Invalid params".to_string(), data: None })
                }
            }
            "add" => {
                if let Some(Value::Array(arr)) = params {
                    if arr.len() == 2 {
                        let a = arr[0].as_i64().unwrap();
                        let b = arr[1].as_i64().unwrap();
                        Ok(json!(a + b))
                    } else {
                        Err(JsonRpcError { code: jsonrpc_errors::INVALID_PARAMS, message: "Invalid params".to_string(), data: None })
                    }
                } else if let Some(Value::Object(map)) = params {
                    let a = map.get("a").unwrap().as_i64().unwrap();
                    let b = map.get("b").unwrap().as_i64().unwrap();
                    Ok(json!(a + b))
                } else {
                    Err(JsonRpcError { code: jsonrpc_errors::INVALID_PARAMS, message: "Invalid params".to_string(), data: None })
                }
            }
            "fail" => Err(JsonRpcError { code: jsonrpc_errors::INTERNAL_ERROR, message: "fail!".to_string(), data: None }),
            _ => Err(JsonRpcError { code: jsonrpc_errors::METHOD_NOT_FOUND, message: "Method not found".to_string(), data: None })
        }
    }
}

struct BadDecoder;
impl JsonDecoder for BadDecoder {
    fn decode(&self, _arg: &str) -> Result<Value, serde_json::Error> {
        Err(serde_json::Error::custom("parsefail"))
    }
}

fn make_req(method: &str, params: Option<Value>, id: i64) -> String {
    let mut m = serde_json::Map::new();
    m.insert("jsonrpc".to_string(), json!("2.0"));
    m.insert("method".to_string(), json!(method));
    m.insert("id".to_string(), json!(id));
    if let Some(p) = params {
        m.insert("params".to_string(), p);
    }
    Value::Object(m).to_string()
}

#[test]
fn test_jsonrpc_result_error_helpers() {
    assert_eq!(jsonrpc_result(17, json!([1, 2])), json!({"jsonrpc":"2.0","result":[1,2],"id":17}));
    let e = jsonrpc_error(5, 1, "err", "trace");
    assert_eq!(e["error"]["code"], 1);
    assert_eq!(e["error"]["data"], "trace");
    assert_eq!(e["id"], 5);
}

#[test]
fn test_jsonrpc_server_call_success_list_params() {
    let req = make_req("add", Some(json!([3,4])), 1);
    let result = jsonrpc_server_call(&DummyTarget, &req, None);
    assert_eq!(result["result"], 7);
}

#[test]
fn test_jsonrpc_server_call_success_dict_params() {
    let req = make_req("add", Some(json!({"a": 10, "b": 7})), 1);
    let result = jsonrpc_server_call(&DummyTarget, &req, None);
    assert_eq!(result["result"], 17);
}

#[test]
fn test_jsonrpc_server_call_success_echo() {
    let req = make_req("echo", Some(json!(["hi"])), 1);
    let result = jsonrpc_server_call(&DummyTarget, &req, None);
    assert_eq!(result["result"], "hi");
}

#[test]
fn test_jsonrpc_server_call_internal_error() {
    let req = make_req("fail", None, 1);
    let result = jsonrpc_server_call(&DummyTarget, &req, None);
    assert_eq!(result["error"]["code"], jsonrpc_errors::INTERNAL_ERROR);
    assert!(result["error"]["message"].as_str().unwrap().contains("fail!"));
}

#[test]
fn test_jsonrpc_server_call_parse_error() {
    let result = jsonrpc_server_call(&DummyTarget, "badjson", Some(&BadDecoder));
    assert_eq!(result["error"]["code"], jsonrpc_errors::PARSE_ERROR);
}

#[test]
fn test_jsonrpc_server_call_invalid_request() {
    for bad in [
        json!({"jsonrpc": "2.0"}).to_string(),
        json!({"jsonrpc": "2.0", "id": 1}).to_string(),
        json!({"jsonrpc": "2.0", "method": "echo"}).to_string()
    ].iter() {
        let result = jsonrpc_server_call(&DummyTarget, bad, None);
        assert_eq!(result["error"]["code"], jsonrpc_errors::INVALID_REQUEST);
    }
}

#[test]
fn test_jsonrpc_server_call_method_not_found() {
    let req = make_req("notfound", None, 1);
    let result = jsonrpc_server_call(&DummyTarget, &req, None);
    assert_eq!(result["error"]["code"], jsonrpc_errors::METHOD_NOT_FOUND);
}