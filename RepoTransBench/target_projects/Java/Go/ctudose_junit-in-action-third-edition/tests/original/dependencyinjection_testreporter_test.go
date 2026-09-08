package original

import (
	"testing"
)

func TestReportSingleValue(t *testing.T) {
	t.Log("Single value")
}

func TestReportKeyValuePair(t *testing.T) {
	t.Logf("%s: %s", "Key", "Value")
}

func TestReportMultipleKeyValuePairs(t *testing.T) {
	values := map[string]string{
		"user":     "John",
		"password": "secret",
	}
	for k, v := range values {
		t.Logf("%s: %s", k, v)
	}
}