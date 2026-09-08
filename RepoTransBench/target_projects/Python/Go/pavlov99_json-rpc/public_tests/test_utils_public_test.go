package public_tests

import (
	"testing"
	"encoding/json"
	"time"
)

func TestPublicISO8601DatetimeFormat(t *testing.T) {
	testTime := time.Date(2020, time.September, 20, 14, 45, 30, 0, time.UTC)
	formatted := testTime.Format("2006-01-02T15:04:05Z")
	expected := "2020-09-20T14:45:30Z"
	if formatted != expected {
		t.Errorf("Expected %s, got %s", expected, formatted)
	}
}

func TestPublicJsonMarshalSimpleStruct(t *testing.T) {
	type Foo struct {
		Bar int `json:"bar"`
	}
	value := Foo{Bar: 123}
	b, err := json.Marshal(value)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	expected := `{"bar":123}`
	if string(b) != expected {
		t.Errorf("Unexpected JSON output: %s", string(b))
	}
}