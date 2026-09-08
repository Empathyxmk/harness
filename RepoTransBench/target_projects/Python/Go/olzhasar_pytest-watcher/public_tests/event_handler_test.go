package public_tests

import (
	"testing"
)

type DummyEvent struct {
	SrcPath string
}

type DummyHandler struct {
	Changed *[]string
}

func (h *DummyHandler) OnModified(event DummyEvent) {
	*h.Changed = append(*h.Changed, "modified")
}

func TestEventHandlerModified(t *testing.T) {
	changed := []string{}
	handler := DummyHandler{Changed: &changed}
	event := DummyEvent{SrcPath: "afile.txt"}
	handler.OnModified(event)
	found := false
	for _, val := range changed {
		if val == "modified" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected 'modified' in changed")
	}
}