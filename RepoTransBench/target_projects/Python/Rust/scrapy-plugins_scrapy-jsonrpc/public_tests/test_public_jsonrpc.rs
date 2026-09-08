use scrapy_jsonrpc::jsonrpc::{jsonrpc_success_obj, jsonrpc_error_obj};
use serde_json::{json, Value};

#[test]
fn test_jsonrpc_success_obj_public() {
    let result = jsonrpc_success_obj("abcde", json!({"value": 99}));
    assert_eq!(result["jsonrpc"], "2.0");
    assert_eq!(result["id"], "abcde");
    assert_eq!(result["result"], json!({"value": 99}));
}

#[test]
fn test_jsonrpc_error_obj_public() {
    let error = jsonrpc_error_obj("xyz01", -123, "Unexpected Error", None);
    assert_eq!(error["jsonrpc"], "2.0");
    assert_eq!(error["id"], "xyz01");
    let err = &error["error"];
    assert_eq!(err["code"], -123);
    assert_eq!(err["message"], "Unexpected Error");
}

#[test]
fn test_jsonrpc_error_obj_with_data_public() {
    let error = jsonrpc_error_obj("ab10", -20, "Message", Some(json!({"details": "extra"})));
    assert_eq!(error["jsonrpc"], "2.0");
    assert_eq!(error["id"], "ab10");
    let err = &error["error"];
    assert_eq!(err["code"], -20);
    assert_eq!(err["message"], "Message");
    assert_eq!(err["data"], json!({"details": "extra"}));
}