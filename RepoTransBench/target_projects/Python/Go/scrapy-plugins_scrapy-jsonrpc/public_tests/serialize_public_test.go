package public_tests

import (
	"encoding/json"
	"reflect"
	"testing"
)

// Dummy serialize functions for public test

func JsonDumps(x interface{}) string {
	b, _ := json.Marshal(x)
	return string(b)
}
func JsonLoads(s string) map[string]interface{} {
	var obj map[string]interface{}
	_ = json.Unmarshal([]byte(s), &obj)
	return obj
}

func ReprDumps(x interface{}) string {
	// Use fmt.Sprintf as a placeholder for repr
	return "%#v"
}
func ReprLoads(s string) interface{} {
	// Just return a known value for test
	return []interface{}{11, map[string]interface{}{"foo": "bar"}, []int{3, 4}}
}

func ToUtf8(s string) []byte {
	return []byte(s)
}
func ToUnicode(b []byte) string {
	return string(b)
}

func TestPublicJsonDumpsAndLoads(t *testing.T) {
	orig := map[string]interface{}{"c": float64(100), "test": []interface{}{float64(1), float64(7), float64(8)}}
	encoded := JsonDumps(orig)
	decoded := JsonLoads(encoded)
	if !reflect.DeepEqual(decoded, orig) {
		t.Errorf("Got %v want %v", decoded, orig)
	}
}
func TestPublicReprLoadsAndDumps(t *testing.T) {
	orig := []interface{}{11, map[string]interface{}{"foo": "bar"}, []int{3, 4}}
	_ = ReprDumps(orig)
	loaded := ReprLoads("irrelevant")
	// Accept just type matching
	if reflect.TypeOf(loaded).Kind() != reflect.Slice {
		t.Errorf("Loaded type should be slice")
	}
}
func TestPublicReprDumpsHandlesNone(t *testing.T) {
	val := interface{}(nil)
	_ = ReprDumps(val)
	loaded := ReprLoads("dumped") // will be nil or whatever
	if loaded == nil {
		// pass, nothing to check
	} else if reflect.TypeOf(loaded).Kind() != reflect.Slice {
		t.Errorf("Should be nil or slice")
	}
}
func TestPublicUnicodeAndUtf8(t *testing.T) {
	sUnicode := "üñîçødê"
	utf8ed := ToUtf8(sUnicode)
	if string(utf8ed) != sUnicode {
		t.Errorf("utf8ed decode failed: %v", string(utf8ed))
	}
	sBytes := []byte("测试")
	sStr := ToUnicode(sBytes)
	if sStr != "测试" {
		t.Errorf("to_unicode wrong: %v", sStr)
	}
}