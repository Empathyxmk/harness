package handlers

import (
	"testing"
)

func TestLocalHandlerEmitsProperly(t *testing.T) {
	event := map[string]interface{}{
		"event_type": "local",
		"details":    "test_local_event",
	}
	got := HandleLocal(event)
	want := "Handled local event: test_local_event"
	if got != want {
		t.Errorf("HandleLocal: got %v, want %v", got, want)
	}
}

func HandleLocal(e map[string]interface{}) string {
	return "Handled local event: " + e["details"].(string)
}