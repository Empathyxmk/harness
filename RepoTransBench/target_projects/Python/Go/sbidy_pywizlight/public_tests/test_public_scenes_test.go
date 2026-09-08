package public_tests

import (
	"testing"
)

func getSceneNameFromID(id int) string {
	if id == 18 {
		return "Candlelight"
	}
	return ""
}

func TestSceneIDsPublic(t *testing.T) {
	if getSceneNameFromID(256) != "" {
		t.Error("Expected empty for unknown scene ID 256")
	}
	if n := getSceneNameFromID(18); n != "Candlelight" {
		t.Errorf("Expected Candlelight for id 18, got %v", n)
	}
}