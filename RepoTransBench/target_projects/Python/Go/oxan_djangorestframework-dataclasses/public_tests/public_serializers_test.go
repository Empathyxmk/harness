package public_tests

import (
	"testing"
)

type Example struct {
	Value string
}

func ExampleSerialize(e Example) map[string]string {
	return map[string]string{"value": e.Value}
}

func ExampleDeserialize(m map[string]string) Example {
	return Example{Value: m["value"]}
}

func TestExampleSerialize(t *testing.T) {
	e := Example{"abc"}
	m := ExampleSerialize(e)
	if m["value"] != "abc" {
		t.Errorf("Expected serialized value 'abc', got %q", m["value"])
	}
}

func TestExampleDeserialize(t *testing.T) {
	m := map[string]string{"value": "zyx"}
	e := ExampleDeserialize(m)
	if e.Value != "zyx" {
		t.Errorf("Expected deserialized value 'zyx', got %q", e.Value)
	}
}