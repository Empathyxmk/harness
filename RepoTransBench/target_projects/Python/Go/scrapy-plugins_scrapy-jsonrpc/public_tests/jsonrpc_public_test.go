package public_tests

import (
	"reflect"
	"testing"
)

// Mock implementation of the required API for testing
func JsonrpcSuccessObj(id string, value map[string]interface{}) map[string]interface{} {
	return map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      id,
		"result":  value,
	}
}
func JsonrpcErrorObj(id string, code int, msg string, data ...map[string]interface{}) map[string]interface{} {
	errObj := map[string]interface{}{
		"code":    code,
		"message": msg,
	}
	if len(data) > 0 {
		errObj["data"] = data[0]
	}
	return map[string]interface{}{
		"jsonrpc": "2.0",
		"id":      id,
		"error":   errObj,
	}
}

func TestJsonrpcSuccessObjPublic(t *testing.T) {
	result := JsonrpcSuccessObj("abcde", map[string]interface{}{"value": 99})
	if result["jsonrpc"] != "2.0" {
		t.Errorf("jsonrpc field wrong: %v", result["jsonrpc"])
	}
	if result["id"] != "abcde" {
		t.Errorf("id wrong: %v", result["id"])
	}
	if !reflect.DeepEqual(result["result"], map[string]interface{}{"value": 99}) {
		t.Errorf("result wrong: %v", result["result"])
	}
}

func TestJsonrpcErrorObjPublic(t *testing.T) {
	errorObj := JsonrpcErrorObj("xyz01", -123, "Unexpected Error")
	if errorObj["jsonrpc"] != "2.0" {
		t.Errorf("jsonrpc field wrong")
	}
	if errorObj["id"] != "xyz01" {
		t.Errorf("id wrong")
	}
	err := errorObj["error"].(map[string]interface{})
	if err["code"] != -123 {
		t.Errorf("code wrong: %v", err["code"])
	}
	if err["message"] != "Unexpected Error" {
		t.Errorf("message wrong: %v", err["message"])
	}
}

func TestJsonrpcErrorObjWithDataPublic(t *testing.T) {
	errorObj := JsonrpcErrorObj("ab10", -20, "Message", map[string]interface{}{"details": "extra"})
	if errorObj["jsonrpc"] != "2.0" {
		t.Errorf("jsonrpc field wrong")
	}
	if errorObj["id"] != "ab10" {
		t.Errorf("id wrong")
	}
	err := errorObj["error"].(map[string]interface{})
	if err["code"] != -20 {
		t.Errorf("code wrong: %v", err["code"])
	}
	if err["message"] != "Message" {
		t.Errorf("message wrong: %v", err["message"])
	}
	if !reflect.DeepEqual(err["data"], map[string]interface{}{"details": "extra"}) {
		t.Errorf("data wrong: %v", err["data"])
	}
}