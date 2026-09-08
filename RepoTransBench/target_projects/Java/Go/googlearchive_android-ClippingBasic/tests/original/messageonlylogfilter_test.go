package original

import (
	"errors"
	"testing"

	"clippingbasic/tests"
)

type RecordingNode struct {
	LastPriority int
	LastTag      string
	LastMsg      string
	LastTr       error
}

func (n *RecordingNode) Println(priority int, tag, msg string, tr error) {
	n.LastPriority = priority
	n.LastTag = tag
	n.LastMsg = msg
	n.LastTr = tr
}

func setupFilter() (*tests.MessageOnlyLogFilter, *RecordingNode) {
	recorder := &RecordingNode{LastPriority: -100, LastTag: "zzz", LastMsg: "uuu"}
	filter := &tests.MessageOnlyLogFilter{}
	filter.SetNext(recorder)
	return filter, recorder
}

func TestPrintlnFiltersToMessageOnly(t *testing.T) {
	filter, recorder := setupFilter()
	filter.Println(tests.INFO, "TAG", "hellomsg", errors.New("should not propagate"))
	if recorder.LastPriority != tests.NONE {
		t.Errorf("Expected priority NONE, got %d", recorder.LastPriority)
	}
	if recorder.LastTag != "" {
		t.Errorf("Expected empty tag, got '%s'", recorder.LastTag)
	}
	if recorder.LastMsg != "hellomsg" {
		t.Errorf("Expected message 'hellomsg', got '%s'", recorder.LastMsg)
	}
	if recorder.LastTr != nil {
		t.Errorf("Expected nil error")
	}
}

func TestConstructorWithNext(t *testing.T) {
	recorder := &RecordingNode{}
	filter := tests.NewMessageOnlyLogFilter(recorder)
	if filter.GetNext() != recorder {
		t.Errorf("Expected Next to match recorder")
	}
}

func TestSetAndGetNext(t *testing.T) {
	recorder := &RecordingNode{}
	f := &tests.MessageOnlyLogFilter{}
	f.SetNext(recorder)
	if f.GetNext() != recorder {
		t.Errorf("Expected Next to match recorder on set")
	}
}

func TestNullNextDoesNothing(t *testing.T) {
	f := &tests.MessageOnlyLogFilter{}
	defer func() {
		if r := recover(); r != nil {
			t.Error("Should not panic when Next is nil")
		}
	}()
	f.Println(tests.ERROR, "x", "yz", nil)
}