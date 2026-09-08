package tests

import (
	"testing"
)

type LogView struct {
	appendToLog func(text string)
	next LogNode
}

func NewLogView() *LogView {
	return &LogView{}
}

func (lv *LogView) Println(priority int, tag, msg string, err error) {
	str := lv.format(priority, tag, msg, err)
	if lv.appendToLog != nil {
		lv.appendToLog(str)
	}
	if lv.next != nil {
		lv.next.Println(priority, tag, msg, err)
	}
}

func (lv *LogView) format(priority int, tag, msg string, err error) string {
	sb := ""
	sb = appendIfNotNull(sb, lv.priorityToString(priority), "\t")
	sb = appendIfNotNull(sb, tag, "\t")
	sb = appendIfNotNull(sb, msg, "\n")
	if err != nil {
		sb = appendIfNotNull(sb, err.Error(), "\n")
	}
	return sb
}
func (lv *LogView) priorityToString(priority int) string {
	switch priority {
	case LogVERBOSE: return "VERBOSE"
	case LogDEBUG: return "DEBUG"
	case LogINFO: return "INFO"
	case LogWARN: return "WARN"
	case LogERROR: return "ERROR"
	case LogASSERT: return "ASSERT"
	default: return "UNKNOWN"
	}
}
func appendIfNotNull(sb, add, del string) string {
	if add != "" && add != "<nil>" && add != "<null>" {
		return sb + add + del
	}
	return sb
}
func (lv *LogView) SetNext(n LogNode) { lv.next = n }
func (lv *LogView) GetNext() LogNode  { return lv.next }

func TestConstructors(t *testing.T) {
	v1 := NewLogView()
	v2 := NewLogView()
	v3 := NewLogView()
	if v1 == nil || v2 == nil || v3 == nil {
		t.Fatal("NewLogView null")
	}
}

func TestAppendIfNotNullBehavior(t *testing.T) {
	sb := "start"
	sb2 := appendIfNotNull(sb, "add", ",")
	if sb2 != "startadd," {
		t.Errorf("Expected 'startadd,', got %q", sb2)
	}
	sb = "x"
	sb2 = appendIfNotNull(sb, "", ",")
	if sb2 != "x" {
		t.Errorf("Expect 'x'")
	}
	sb = ""
	sb2 = appendIfNotNull(sb, "", "|")
	if sb2 != "" {
		t.Errorf("Expect ''")
	}
}

func TestPrintlnFormatsAndAppends(t *testing.T) {
	output := ""
	v := &LogView{
		appendToLog: func(s string) { output = s },
	}
	v.Println(LogWARN, "tag1", "msg1", nil)
	if !(contains(output, "WARN") && contains(output, "tag1") && contains(output, "msg1")) {
		t.Errorf("Println(WARN) output: %s", output)
	}
	output = ""
	v.Println(LogERROR, "tag2", "msg2", createError("Test"))
	if !(contains(output, "ERROR") && contains(output, "msg2") && contains(output, "Test")) {
		t.Errorf("Println(ERROR, err) output: %s", output)
	}
	// test next
	mock := makeMockNode()
	v.SetNext(mock)
	v.Println(LogINFO, "tagx", "msgx", nil)
	if len(mock.calls) == 0 {
		t.Errorf("Next not called")
	}
}

func TestSetAndGetNext(t *testing.T) {
	v := NewLogView()
	if v.GetNext() != nil {
		t.Errorf("Next should init nil")
	}
	ln := makeMockNode()
	v.SetNext(ln)
	if v.GetNext() != ln {
		t.Errorf("Next mismatch")
	}
}

func createError(msg string) error { return &errorString{msg} }
type errorString struct{ s string }
func (e *errorString) Error() string { return e.s }

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || len(s) >= len(sub) && (s[0:len(sub)] == sub || contains(s[1:], sub)))
}