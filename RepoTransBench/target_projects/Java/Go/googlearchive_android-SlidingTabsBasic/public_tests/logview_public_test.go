package public_tests

import (
	"testing"
)

type LogNode interface {
	Println(priority int, tag, msg string, err error)
}

type LogView struct {
	appendToLog func(text string)
	next        LogNode
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
	case 2:
		return "VERBOSE"
	case 3:
		return "DEBUG"
	case 4:
		return "INFO"
	case 5:
		return "WARN"
	case 6:
		return "ERROR"
	case 7:
		return "ASSERT"
	default:
		return "UNKNOWN"
	}
}
func (lv *LogView) SetNext(n LogNode) { lv.next = n }
func (lv *LogView) GetNext() LogNode  { return lv.next }

// Utility for appendIfNotNull
func appendIfNotNull(sb, add, del string) string {
	if add != "" && add != "<nil>" && add != "<null>" {
		return sb + add + del
	}
	return sb
}

func TestAllConstructors(t *testing.T) {
	v1 := &LogView{}
	v2 := &LogView{}
	v3 := &LogView{}
	if v1 == nil || v2 == nil || v3 == nil {
		t.Fatal("LogView creation failed")
	}
}

func TestAppendIfNotNullEdgeCases(t *testing.T) {
	sb := "public"
	sb2 := appendIfNotNull(sb, "append", "|")
	if sb2 != "publicappend|" {
		t.Errorf("appendIfNotNull failed")
	}
	sb = "q"
	sb2 = appendIfNotNull(sb, "", "|")
	if sb2 != "q" {
		t.Errorf("appendIfNotNull fail empty")
	}
	sb = ""
	sb2 = appendIfNotNull(sb, "", ";")
	if sb2 != "" {
		t.Errorf("appendIfNotNull all empty")
	}
}

func TestPrintlnWithPublicData(t *testing.T) {
	output := ""
	v := &LogView{
		appendToLog: func(s string) { output = s },
	}
	v.Println(4, "tagPublic1", "msgInfo", nil)
	if !(contains(output, "INFO") && contains(output, "tagPublic1") && contains(output, "msgInfo")) {
		t.Errorf("Println INFO output: %s", output)
	}
	output = ""
	v.Println(3, "tagPublic2", "msgDebug", createError("InvalidArg"))
	if !(contains(output, "DEBUG") && contains(output, "msgDebug") && contains(output, "InvalidArg")) {
		t.Errorf("Println DEBUG/err output: %s", output)
	}
	// Next node test
	mock := &logNodeMock{}
	v.SetNext(mock)
	v.Println(2, "tagP", "msgP", nil)
	// Asserts that Println was called on next: last call is (2,tagP,msgP,nil)
	c := mock.last
	if !(c.Priority == 2 && c.Tag == "tagP" && c.Msg == "msgP" && c.Err == nil) {
		t.Errorf("Next not called correctly: %+v", c)
	}
}

func TestSetGetNextNodePublic(t *testing.T) {
	v := &LogView{}
	if v.GetNext() != nil {
		t.Errorf("Next should init nil")
	}
	mock := &logNodeMock{}
	v.SetNext(mock)
	if v.GetNext() != mock {
		t.Errorf("Next mismatch")
	}
}

func createError(msg string) error { return &errorString{msg} }
type errorString struct{ s string }
func (e *errorString) Error() string { return e.s }

func contains(s, sub string) bool {
	return len(s) >= len(sub) && (s == sub || len(s) >= len(sub) && (s[0:len(sub)] == sub || contains(s[1:], sub)))
}