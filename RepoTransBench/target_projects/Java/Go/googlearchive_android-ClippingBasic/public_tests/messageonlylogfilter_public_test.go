package public_tests

import (
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
	recorder := &RecordingNode{LastPriority: 1000, LastTag: "abc", LastMsg: "zzz"}
	filter := &tests.MessageOnlyLogFilter{}
	filter.SetNext(recorder)
	return filter, recorder
}

func TestPrintlnFiltersToMessageOnlyPublic(t *testing.T) {
	filter, recorder := setupFilter()
	filter.Println(tests.WARN, "PUBTAG", "public message", &customErr{"not seen"})
	if recorder.LastPriority != tests.NONE {
		t.Errorf("Expected priority NONE, got %d (Public)", recorder.LastPriority)
	}
	if recorder.LastTag != "" {
		t.Errorf("Expected empty tag, got '%s' (Public)", recorder.LastTag)
	}
	if recorder.LastMsg != "public message" {
		t.Errorf("Expected message 'public message', got '%s' (Public)", recorder.LastMsg)
	}
	if recorder.LastTr != nil {
		t.Errorf("Expected nil error (Public)")
	}
}

func TestConstructorWithNextPublic(t *testing.T) {
	recorder := &RecordingNode{}
	filter := tests.NewMessageOnlyLogFilter(recorder)
	if filter.GetNext() != recorder {
		t.Errorf("Expected Next to match recorder (Public)")
	}
}

func TestSetAndGetNextPublic(t *testing.T) {
	recorder := &RecordingNode{}
	f := &tests.MessageOnlyLogFilter{}
	f.SetNext(recorder)
	if f.GetNext() != recorder {
		t.Errorf("Expected Next to match recorder on set (Public)")
	}
}

func TestNullNextDoesNothingPublic(t *testing.T) {
	f := &tests.MessageOnlyLogFilter{}
	defer func() {
		if r := recover(); r != nil {
			t.Error("Should not panic when Next is nil (Public)")
		}
	}()
	f.Println(tests.VERBOSE, "v", "pqrs", nil)
}

type customErr struct{ msg string }
func (c *customErr) Error() string { return c.msg }