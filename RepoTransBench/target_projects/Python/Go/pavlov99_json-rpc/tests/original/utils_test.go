package original

import (
	"testing"
	"encoding/json"
	"time"
)

func TestISO8601DatetimeFormat(t *testing.T) {
	testTime := time.Date(2021, time.June, 7, 13, 5, 0, 0, time.UTC)
	result := testTime.Format("2006-01-02T15:04:05Z")
	expected := "2021-06-07T13:05:00Z"
	if result != expected {
		t.Errorf("Expected %s, got %s", expected, result)
	}
}

func TestJsonMarshalFloatPrecision(t *testing.T) {
	value := struct {
		Number float64 `json:"number"`
	}{Number: 1.23456789}
	b, err := json.Marshal(value)
	if err != nil {
		t.Fatalf("Marshal failed: %v", err)
	}
	expected := `{"number":1.23456789}`
	got := string(b)
	if got != expected {
		t.Errorf("Unexpected JSON output: %s", got)
	}
}