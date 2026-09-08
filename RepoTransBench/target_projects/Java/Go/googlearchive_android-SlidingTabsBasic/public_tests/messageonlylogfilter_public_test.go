package public_tests

import (
	"testing"
)

type LogNode interface {
	Println(priority int, tag, msg string, err error)
}
type logNodeMock struct {
	last struct {
		Priority int
		Tag      string
		Msg      string
		Err      error
	}
}

func (m *logNodeMock) Println(priority int, tag, msg string, err error) {
	m.last.Priority, m.last.Tag, m.last.Msg, m.last.Err = priority, tag, msg, err
}

type MessageOnlyLogFilter struct {
	next LogNode
}

func (f *MessageOnlyLogFilter) SetNext(n LogNode) {
	f.next = n
}
func (f *MessageOnlyLogFilter) GetNext() LogNode {
	return f.next
}
func (f *MessageOnlyLogFilter) Println(priority int, tag, msg string, err error) {
	if f.next != nil {
		f.next.Println(priority, "", msg, nil)
	}
}

func TestFiltersMessageOnlyDifferentInput(t *testing.T) {
	filter := &MessageOnlyLogFilter{}
	mock := &logNodeMock{}
	filter.SetNext(mock)
	filter.Println(99, "PublicTAG", "HelloWorldMsg", nil)
	c := mock.last
	if !(c.Priority == 99 && c.Tag == "" && c.Msg == "HelloWorldMsg" && c.Err == nil) {
		t.Errorf("MessageOnlyLogFilter mismatch: %+v", c)
	}
}

func TestNoNextNodeIsSafePublic(t *testing.T) {
	filter := &MessageOnlyLogFilter{}
	filter.Println(88, "AnotherTAG", "SomeMessage", nil)
	// Should not panic
}

func TestChainedNextNodePublic(t *testing.T) {
	filter := &MessageOnlyLogFilter{}
	mock := &logNodeMock{}
	filter.SetNext(mock)
	filter.Println(5, "TagChain", "ChainedMsg", createError("publicChain"))
	c := mock.last
	if !(c.Priority == 5 && c.Tag == "" && c.Msg == "ChainedMsg" && c.Err == nil) {
		t.Errorf("Chained next mismatch: %+v", c)
	}
}

func createError(msg string) error { return &errorString{msg} }
type errorString struct{ s string }
func (e *errorString) Error() string { return e.s }