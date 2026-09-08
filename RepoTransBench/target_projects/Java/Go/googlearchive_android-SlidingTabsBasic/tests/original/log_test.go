package tests

import (
	"errors"
	"testing"
)

type realLogNode struct {
	last struct{
		Priority int
		Tag string
		Msg string
		Err error
	}
	calls []struct{
		Priority int
		Tag string
		Msg string
		Err error
	}
}
func (ln *realLogNode) Println(priority int, tag, msg string, err error) {
	ln.last.Priority, ln.last.Tag, ln.last.Msg, ln.last.Err = priority, tag, msg, err
	ln.calls = append(ln.calls, ln.last)
}
func (ln *realLogNode) LastCall() (priority int, tag, msg string, err error) {
	return ln.last.Priority, ln.last.Tag, ln.last.Msg, ln.last.Err
}

func makeMockNode() *realLogNode {
	return &realLogNode{}
}

// Mimic Log static functionality
type LogType struct{
	node LogNode
}
var Log LogType

func (l *LogType) SetLogNode(n LogNode) {
	l.node = n
}
func (l *LogType) GetLogNode() LogNode {
	return l.node
}

var (
	LogVERBOSE = 2
	LogDEBUG = 3
	LogINFO  = 4
	LogWARN  = 5
	LogERROR = 6
	LogASSERT = 7
	LogNONE = 0
)

func (l *LogType) Println(priority int, tag, msg string, err error) {
	if l.node != nil {
		l.node.Println(priority, tag, msg, err)
	}
}
func (l *LogType) V(tag, msg string, err ...error)        { l.Println(LogVERBOSE, tag, msg, getErrArg(err...)) }
func (l *LogType) D(tag, msg string, err ...error)        { l.Println(LogDEBUG, tag, msg, getErrArg(err...)) }
func (l *LogType) I(tag, msg string, err ...error)        { l.Println(LogINFO, tag, msg, getErrArg(err...)) }
func (l *LogType) W(tag, msg string, err ...error)        { l.Println(LogWARN, tag, msg, getErrArg(err...)) }
func (l *LogType) E(tag, msg string, err ...error)        { l.Println(LogERROR, tag, msg, getErrArg(err...)) }
func (l *LogType) Wtf(tag, msg string, err ...error)      { l.Println(LogASSERT, tag, msg, getErrArg(err...)) }

func getErrArg(err ...error) error {
	if len(err) > 0 {
		return err[0]
	}
	return nil
}

func TestSetAndGetLogNode(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	if Log.GetLogNode() != mock {
		t.Errorf("Expected node set/get match")
	}
}

func TestPrintlnCallsNode(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.Println(LogDEBUG, "TAG", "msg", nil)
	priority, tag, msg, err := mock.LastCall()
	if !(priority == LogDEBUG && tag == "TAG" && msg == "msg" && err == nil) {
		t.Errorf("Println missing, got %d/%s/%s/%v", priority, tag, msg, err)
	}
	Log.Println(LogINFO, "TAG2", "msg2", nil)
	priority, tag, msg, err = mock.LastCall()
	if !(priority == LogINFO && tag == "TAG2" && msg == "msg2" && err == nil) {
		t.Errorf("Println INFO variant failed")
	}
}

func TestVerbosityDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.V("V", "verbose")
	if mock.last.Priority != LogVERBOSE || mock.last.Tag != "V" || mock.last.Msg != "verbose" || mock.last.Err != nil {
		t.Errorf("V() failed %v", mock.last)
	}
	Log.V("V2", "verbose2", errors.New("err"))
	if mock.last.Priority != LogVERBOSE || mock.last.Tag != "V2" || mock.last.Msg != "verbose2" || mock.last.Err == nil {
		t.Errorf("V() with error failed")
	}
}

func TestDebugDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.D("D", "debug")
	if mock.last.Priority != LogDEBUG || mock.last.Tag != "D" || mock.last.Msg != "debug" || mock.last.Err != nil {
		t.Errorf("D() failed %v", mock.last)
	}
	Log.D("D2", "debug2", errors.New("err"))
	if mock.last.Priority != LogDEBUG || mock.last.Tag != "D2" || mock.last.Msg != "debug2" || mock.last.Err == nil {
		t.Errorf("D() with err failed")
	}
}

func TestInfoDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.I("I", "info")
	if mock.last.Priority != LogINFO || mock.last.Tag != "I" || mock.last.Msg != "info" || mock.last.Err != nil {
		t.Errorf("I() failed")
	}
	Log.I("I2", "info2", errors.New("err"))
	if mock.last.Priority != LogINFO || mock.last.Tag != "I2" || mock.last.Msg != "info2" || mock.last.Err == nil {
		t.Errorf("I() with err failed")
	}
}

func TestWarnDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.W("W", "warn")
	if mock.last.Priority != LogWARN || mock.last.Tag != "W" || mock.last.Msg != "warn" || mock.last.Err != nil {
		t.Errorf("W() failed")
	}
	Log.W("W2", "warn2", errors.New("err"))
	if mock.last.Priority != LogWARN || mock.last.Tag != "W2" || mock.last.Msg != "warn2" || mock.last.Err == nil {
		t.Errorf("W() with err failed")
	}
}

func TestErrorDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.E("E", "error")
	if mock.last.Priority != LogERROR || mock.last.Tag != "E" || mock.last.Msg != "error" || mock.last.Err != nil {
		t.Errorf("E() failed")
	}
	Log.E("E2", "error2", errors.New("err"))
	if mock.last.Priority != LogERROR || mock.last.Tag != "E2" || mock.last.Msg != "error2" || mock.last.Err == nil {
		t.Errorf("E() with err failed")
	}
}

func TestWtfDelegates(t *testing.T) {
	mock := makeMockNode()
	Log.SetLogNode(mock)
	Log.Wtf("T", "assert")
	if mock.last.Priority != LogASSERT || mock.last.Tag != "T" || mock.last.Msg != "assert" || mock.last.Err != nil {
		t.Errorf("Wtf() failed")
	}
	Log.Wtf("T2", "assert2", errors.New("err"))
	if mock.last.Priority != LogASSERT || mock.last.Tag != "T2" || mock.last.Msg != "assert2" || mock.last.Err == nil {
		t.Errorf("Wtf() with err failed")
	}
}

func TestNoNodeDoesNotCrash(t *testing.T) {
	Log.SetLogNode(nil)
	// Should not panic
	Log.D("TAG", "Should do nothing")
}