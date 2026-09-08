package public

import (
	"testing"
)

func ParseConfig(s string) (string, error) {
	if s == "bad" {
		return "", errBadConfig
	}
	return "parsed", nil
}

var errBadConfig = &BadConfigError{}

type BadConfigError struct{}

func (e *BadConfigError) Error() string {
	return "bad config"
}

func TestParseConfig(t *testing.T) {
	res, err := ParseConfig("good")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if res != "parsed" {
		t.Errorf("ParseConfig(\"good\") = %q, want \"parsed\"", res)
	}

	_, err2 := ParseConfig("bad")
	if err2 == nil {
		t.Fatalf("expected error for input 'bad', got nil")
	}
	if err2.Error() != "bad config" {
		t.Errorf("unexpected error text: %v", err2)
	}
}