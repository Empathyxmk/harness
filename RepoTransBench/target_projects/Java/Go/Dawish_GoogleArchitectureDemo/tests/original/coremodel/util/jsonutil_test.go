package util

import (
	"encoding/json"
	"strings"
	"testing"
)

type Bean struct {
	Field1 string `json:"field1"`
	Field2 int    `json:"field2"`
}

func (a Bean) Equals(b Bean) bool {
	return a.Field1 == b.Field1 && a.Field2 == b.Field2
}

// Simulate what JsonUtil.Str2JsonBean does in Java: Parse JSON into a struct.
func Str2JsonBean[T any](s string, out *T) error {
	return json.Unmarshal([]byte(s), out)
}

// Simulate what JsonUtil.JsonBean2Str does in Java: Serializes struct to JSON.
func JsonBean2Str(v interface{}) string {
	data, err := json.Marshal(v)
	if err != nil {
		return ""
	}
	return string(data)
}

// Simulate what JsonUtil.JsonList2Str does in Java: Serializes slice to JSON array.
// Returns empty string for nil/empty, like Java test treats empty input as null (so returns nil or "null").
func JsonList2Str[T any](xs []T) string {
	if len(xs) == 0 {
		return ""
	}
	data, err := json.Marshal(xs)
	if err != nil {
		return ""
	}
	return string(data)
}

func TestStr2JsonBean_ValidJson(t *testing.T) {
	jsonStr := `{"field1":"test","field2":123}`
	var bean Bean
	err := Str2JsonBean(jsonStr, &bean)
	if err != nil {
		t.Fatalf("Str2JsonBean failed: %v", err)
	}
	if bean.Field1 != "test" {
		t.Errorf("expected field1 to be 'test', got %v", bean.Field1)
	}
	if bean.Field2 != 123 {
		t.Errorf("expected field2 to be 123, got %d", bean.Field2)
	}
}

func TestStr2JsonBean_InvalidJson(t *testing.T) {
	jsonStr := `{field1:test,field2:abc}`
	var bean Bean
	err := Str2JsonBean(jsonStr, &bean)
	if err == nil {
		t.Errorf("expected error for invalid json, got none")
	}
}

func TestJsonBean2Str_Valid(t *testing.T) {
	bean := Bean{"abc", 42}
	jsonStr := JsonBean2Str(bean)
	if jsonStr == "" {
		t.Fatal("expected non-empty json")
	}
	if !strings.Contains(jsonStr, `"field1":"abc"`) && !strings.Contains(jsonStr, `"field1": "abc"`) {
		t.Error(`expected json to contain '"field1":"abc"'`)
	}
	if !strings.Contains(jsonStr, `"field2":42`) && !strings.Contains(jsonStr, `"field2": 42`) {
		t.Error(`expected json to contain '"field2":42'`)
	}
}

func TestJsonBean2Str_Null(t *testing.T) {
	var bean *Bean = nil
	jsonStr := JsonBean2Str(bean)
	// json.Marshal(nil) returns "null"
	if jsonStr != "null" {
		t.Errorf("expected json to be 'null', got %s", jsonStr)
	}
}

func TestJsonList2Str_EmptyList(t *testing.T) {
	var list []Bean
	res := JsonList2Str(list)
	if res != "" {
		t.Errorf("expected empty string for empty list, got %s", res)
	}
}

func TestJsonList2Str_Multiple(t *testing.T) {
	b1 := Bean{"a", 1}
	b2 := Bean{"b", 2}
	list := []Bean{b1, b2}
	res := JsonList2Str(list)
	if res == "" {
		t.Fatal("expected non-empty result")
	}
	if !(strings.HasPrefix(res, "[") && strings.HasSuffix(res, "]")) {
		t.Errorf("expected result to start with '[' and end with ']'")
	}
	if !strings.Contains(res, `"field1":"a"`) && !strings.Contains(res, `"field1": "a"`) {
		t.Error("missing 'field1:a'")
	}
	if !strings.Contains(res, `"field1":"b"`) && !strings.Contains(res, `"field1": "b"`) {
		t.Error("missing 'field1:b'")
	}
	if !strings.Contains(res, ",") {
		t.Error("missing comma between elements")
	}
}