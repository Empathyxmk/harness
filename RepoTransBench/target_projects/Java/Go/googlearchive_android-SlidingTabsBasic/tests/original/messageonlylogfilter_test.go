package tests

import (
	"testing"
)

type MessageOnlyLogFilter struct{
	next LogNode
}

func NewMessageOnlyLogFilter(next LogNode) *MessageOnlyLogFilter {
	return &MessageOnlyLogFilter{next: next}
}
func (f *MessageOnlyLogFilter) Println(priority int, tag, msg string, err error) {
	if f.next != nil {
		f.next.Println(LogNONE, "", msg, nil)
	}
}
func (f *MessageOnlyLogFilter) SetNext(n LogNode){
	f.next = n
}
func (f *MessageOnlyLogFilter) GetNext() LogNode {
	return f.next
}

func TestMessageOnlyForwarded(t *testing.T) {
	mock := makeMockNode()
	filter := NewMessageOnlyLogFilter(mock)
	filter.Println(LogWARN, "Tag", "Message", createError("err"))
	c := mock.last
	if !(c.Priority == LogNONE && c.Tag == "" && c.Msg == "Message" && c.Err == nil) {
		t.Errorf("MessageOnly did not forward expected values, got %+v", c)
	}
}

func TestNoNextDoesNothing(t *testing.T) {
	filter := NewMessageOnlyLogFilter(nil)
	// Should do nothing / not panic
	filter.Println(LogERROR, "tag", "sample", nil)
}

func TestSetGetNext(t *testing.T) {
	filter := NewMessageOnlyLogFilter(nil)
	if filter.GetNext() != nil {
		t.Errorf("Initial next should be nil")
	}
	mock := makeMockNode()
	filter.SetNext(mock)
	if filter.GetNext() != mock {
		t.Errorf("SetNext/next mismatch")
	}
}