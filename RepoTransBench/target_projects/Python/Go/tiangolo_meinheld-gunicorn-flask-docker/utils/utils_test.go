package utils

import (
	"testing"
)

type DummyContainerHelper struct{}
func (c *DummyContainerHelper) Top() (map[string]interface{}, error) {
	return map[string]interface{}{
		"Processes": [][]string{{"foo", "gunicorn bar"}},
	}, nil
}

func TestGetProcessNamesHelper(t *testing.T) {
	c := &DummyContainerHelper{}
	names, err := GetProcessNames(c)
	if err != nil {
		t.Fatalf("GetProcessNames returned err: %v", err)
	}
	if len(names) != 1 || names[0] != "gunicorn bar" {
		t.Fatalf("Expected [gunicorn bar], got %#v", names)
	}
}

func TestUtf8ValidForAscii(t *testing.T) {
	data := []byte("abc123")
	if !utf8Valid(data) {
		t.Errorf("Expected ascii bytes to be valid utf8")
	}
}

func TestUtf8ValidForBad(t *testing.T) {
	data := []byte{0xff}
	if utf8Valid(data) {
		t.Errorf("Expected 0xff to be invalid utf8")
	}
}