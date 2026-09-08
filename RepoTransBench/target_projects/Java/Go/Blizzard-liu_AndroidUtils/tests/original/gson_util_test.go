package original

import (
    "encoding/json"
    "fmt"
    "reflect"
    "testing"
)

func TestParseMapToJsonValidMap(t *testing.T) {
    m := map[string]string{"foo": "bar"}
    b, err := json.Marshal(m)
    if err != nil {
        t.Fatalf("json.Marshal failed: %v", err)
    }
    s := string(b)
    if _, ok := m["foo"]; !ok || !containsSubstr(s, `"foo":"bar"`) {
        t.Errorf("Expected foo:bar in json, got %q", s)
    }
}

func TestParseMapToJsonNull(t *testing.T) {
    var m map[string]string
    b, err := json.Marshal(m)
    if err != nil {
        t.Fatalf("json.Marshal failed: %v", err)
    }
    s := string(b)
    if s != "null" {
        t.Errorf("Expected json null, got %q", s)
    }
}

type testBean struct {
    Name string `json:"name"`
    Age  int    `json:"age"`
}

func TestParseJsonToBeanValidJson(t *testing.T) {
    jsonStr := `{"name":"Alice", "age":30}`
    var b testBean
    if err := json.Unmarshal([]byte(jsonStr), &b); err != nil {
        t.Fatalf("unmarshal failed: %v", err)
    }
    if b.Name != "Alice" || b.Age != 30 {
        t.Errorf("Expected Alice,30; got %v,%v", b.Name, b.Age)
    }
}

func TestParseJsonToBeanInvalidJson(t *testing.T) {
    jsonStr := `{name:Alice, age:30}`
    var b testBean
    err := json.Unmarshal([]byte(jsonStr), &b)
    if err == nil {
        t.Fatal("Expected error on invalid json, but got none")
    }
}

func TestParseJsonToMapValidJson(t *testing.T) {
    jsonStr := `{"foo":"bar","num":42}`
    var m map[string]interface{}
    if err := json.Unmarshal([]byte(jsonStr), &m); err != nil {
        t.Fatalf("unmarshal failed: %v", err)
    }
    if m["foo"] != "bar" {
        t.Errorf("expected foo == bar, got %v", m["foo"])
    }
    // Go JSON returns float64 for numbers by default
    if m["num"] != float64(42) {
        t.Errorf("Expected num == 42.0, got %v (%v)", m["num"], reflect.TypeOf(m["num"]))
    }
}

func TestParseJsonToMapInvalidJson(t *testing.T) {
    jsonStr := `{foo:bar,num:42}`
    var m map[string]interface{}
    err := json.Unmarshal([]byte(jsonStr), &m)
    if err == nil {
        t.Error("Expected error for invalid json, got none")
    }
}

func TestParseJsonToListValid(t *testing.T) {
    exp := []testBean{{Name: "A", Age: 1}, {Name: "B", Age: 2}}
    jsonStr := `[{"name":"A","age":1},{"name":"B","age":2}]`
    var res []testBean
    if err := json.Unmarshal([]byte(jsonStr), &res); err != nil {
        t.Fatalf("Unmarshal failed: %v", err)
    }
    if len(res) != 2 {
        t.Fatalf("Expected size 2, got %d", len(res))
    }
    if res[0] != exp[0] || res[1] != exp[1] {
        t.Errorf("Output mismatch: got %v, want %v", res, exp)
    }
}

func TestParseJsonToListInvalid(t *testing.T) {
    jsonStr := "[{name:A,age:1},{name:B,age:2}]"
    var res []testBean
    err := json.Unmarshal([]byte(jsonStr), &res)
    if err == nil {
        t.Error("Expected error on invalid json list, but got none")
    }
}

func TestGetFieldValueValid(t *testing.T) {
    jsonStr := `{"key":"value","other":"x"}`
    var m map[string]interface{}
    if err := json.Unmarshal([]byte(jsonStr), &m); err != nil {
        t.Fatalf("Unmarshal failed: %v", err)
    }
    v, _ := m["key"].(string)
    if v != "value" {
        t.Errorf("expected 'value', got %v", v)
    }
}

func TestGetFieldValueKeyNotPresent(t *testing.T) {
    jsonStr := `{"key1":"value1"}`
    var m map[string]interface{}
    if err := json.Unmarshal([]byte(jsonStr), &m); err != nil {
        t.Fatalf("Unmarshal failed: %v", err)
    }
    v, ok := m["missing"].(string)
    if ok {
        t.Errorf("Expected missing key to return nothing, got %v", v)
    }
}

func TestGetFieldValueEmptyJson(t *testing.T) {
    jsonStr := ""
    var m map[string]interface{}
    err := json.Unmarshal([]byte(jsonStr), &m)
    if err == nil {
        t.Errorf("Expected error parsing empty string")
    }
}

func TestGetFieldValueInvalidJson(t *testing.T) {
    jsonStr := "{key:value}"
    var m map[string]interface{}
    err := json.Unmarshal([]byte(jsonStr), &m)
    if err == nil {
        t.Errorf("Expected error parsing invalid json")
    }
}

func containsSubstr(s, substr string) bool {
    return len(s) >= len(substr) && filtersubstring(s, substr)
}
func filtersubstring(s string, substr string) bool {
    for i := 0; i <= len(s)-len(substr); i++ {
        if s[i:i+len(substr)] == substr {
            return true
        }
    }
    return false
}