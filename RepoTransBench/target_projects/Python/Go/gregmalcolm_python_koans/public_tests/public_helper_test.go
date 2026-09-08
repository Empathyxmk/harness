package public_tests

import (
	"testing"
)

func helperClsName(x interface{}) string {
	switch x.(type) {
	case bool:
		return "bool"
	case []interface{}:
		return "tuple" // Just for public test
	}
	return "unknown"
}

func TestPublicClsNameForBool(t *testing.T) {
	if helperClsName(true) != "bool" {
		t.Error("expected 'bool'")
	}
}

func TestPublicClsNameForTuple(t *testing.T) {
	tuple := []interface{}{1}
	if helperClsName(tuple) != "tuple" {
		t.Error("expected 'tuple'")
	}
}