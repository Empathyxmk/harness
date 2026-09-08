package public_tests

import (
	"errors"
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

type LogType struct {
	node LogNode
}

var Log LogType

func (l *LogType) SetLogNode(n LogNode) {
	l.node = n
}
func (l *LogType) GetLogNode() LogNode {
	return l.node
}

const (
	LogVERBOSE = 2
	LogDEBUG   = 3
	LogINFO    = 4
	LogWARN    = 5
	LogERROR   = 6
	LogASSERT  = 7
	LogNONE    = 0
)

func (l *LogType) Println(priority int, tag, msg string, err error) {
	if l.node != nil {
		l.node.Println(priority, tag, msg, err)
	}
}
func (l *LogType) V(tag, msg string, err ...error)   { l.Println(LogVERBOSE, tag, msg, getErrArg(err...)) }
func (l *LogType) D(tag, msg string, err ...error)   { l.Println(LogDEBUG, tag, msg, getErrArg(err...)) }
func (l *LogType) I(tag, msg string, err ...error)   { l.Println(LogINFO, tag, msg, getErrArg(err...)) }
func (l *LogType) W(tag, msg string, err ...error)   { l.Println(LogWARN, tag, msg, getErrArg(err...)) }
func (l *LogType) E(tag, msg string, err ...error)   { l.Println(LogERROR, tag, msg, getErrArg(err...)) }
func (l *LogType) Wtf(tag, msg string, err ...error) { l.Println(LogASSERT, tag, msg, getErrArg(err...)) }

func getErrArg(err ...error) error {
	if len(err) > 0 {
		return err[0]
	}
	return nil
}

func TestSetAndGetLogNodePublic(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	if Log.GetLogNode() != mock {
		t.Errorf("Expected mock for Set/Get")
	}
}

func TestPrintlnCallsNodeWithDifferentValues(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.Println(LogINFO, "PUB_TAG", "publicMsg", nil)
	if !(mock.last.Priority == LogINFO && mock.last.Tag == "PUB_TAG" && mock.last.Msg == "publicMsg" && mock.last.Err == nil) {
		t.Errorf("Println did not call expected")
	}
	Log.Println(LogWARN, "PUB_TAG_WARN", "warnMsg", nil)
	if !(mock.last.Priority == LogWARN && mock.last.Tag == "PUB_TAG_WARN" && mock.last.Msg == "warnMsg" && mock.last.Err == nil) {
		t.Errorf("Println WARN not matching")
	}
}

func TestVerboseDelegatesWithDifferentInput(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.V("VerboseTag", "verbMsg")
	if !(mock.last.Priority == LogVERBOSE && mock.last.Tag == "VerboseTag" && mock.last.Msg == "verbMsg" && mock.last.Err == nil) {
		t.Errorf("V() mismatch")
	}
	Log.V("VerbTag2", "verbMsg2", errors.New("public"))
	if !(mock.last.Priority == LogVERBOSE && mock.last.Tag == "VerbTag2" && mock.last.Msg == "verbMsg2" && mock.last.Err != nil) {
		t.Errorf("V() with err mismatch")
	}
}

func TestDebugDelegatesWithDifferentInput(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.D("DebugTag", "debugMessage")
	if !(mock.last.Priority == LogDEBUG && mock.last.Tag == "DebugTag" && mock.last.Msg == "debugMessage" && mock.last.Err == nil) {
		t.Errorf("D() mismatch")
	}
	Log.D("DebugTag2", "debugMessage2", errors.New("failure"))
	if !(mock.last.Priority == LogDEBUG && mock.last.Tag == "DebugTag2" && mock.last.Msg == "debugMessage2" && mock.last.Err != nil) {
		t.Errorf("D() err mismatch")
	}
}

func TestInfoDelegatesWithPublicData(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.I("InfoTag", "infoMsg1")
	if !(mock.last.Priority == LogINFO && mock.last.Tag == "InfoTag" && mock.last.Msg == "infoMsg1" && mock.last.Err == nil) {
		t.Errorf("I() mismatch")
	}
	Log.I("InfoTag2", "infoMsg2", errors.New("infoNull"))
	if !(mock.last.Priority == LogINFO && mock.last.Tag == "InfoTag2" && mock.last.Msg == "infoMsg2" && mock.last.Err != nil) {
		t.Errorf("I() err mismatch")
	}
}

func TestWarnDelegatesPublic(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.W("WarnTag", "warnMsg1")
	if !(mock.last.Priority == LogWARN && mock.last.Tag == "WarnTag" && mock.last.Msg == "warnMsg1" && mock.last.Err == nil) {
		t.Errorf("W() mismatch")
	}
	Log.W("WarnTag2", "warnMsg2", errors.New("warnArith"))
	if !(mock.last.Priority == LogWARN && mock.last.Tag == "WarnTag2" && mock.last.Msg == "warnMsg2" && mock.last.Err != nil) {
		t.Errorf("W() with err mismatch")
	}
}

func TestErrorDelegatesPublic(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.E("ErrorTag", "errorMsg1")
	if !(mock.last.Priority == LogERROR && mock.last.Tag == "ErrorTag" && mock.last.Msg == "errorMsg1" && mock.last.Err == nil) {
		t.Errorf("E() mismatch")
	}
	Log.E("ErrorTag2", "errorMsg2", errors.New("publicError"))
	if !(mock.last.Priority == LogERROR && mock.last.Tag == "ErrorTag2" && mock.last.Msg == "errorMsg2" && mock.last.Err != nil) {
		t.Errorf("E() with err mismatch")
	}
}

func TestWtfDelegatesWithDifferentData(t *testing.T) {
	mock := &logNodeMock{}
	Log.SetLogNode(mock)
	Log.Wtf("AssertT", "assertMsg")
	if !(mock.last.Priority == LogASSERT && mock.last.Tag == "AssertT" && mock.last.Msg == "assertMsg" && mock.last.Err == nil) {
		t.Errorf("Wtf() mismatch")
	}
	Log.Wtf("AssertT2", "assertMsg2", errors.New("assertThrowable"))
	if !(mock.last.Priority == LogASSERT && mock.last.Tag == "AssertT2" && mock.last.Msg == "assertMsg2" && mock.last.Err != nil) {
		t.Errorf("Wtf() with err mismatch")
	}
}

func TestNoNodeSafeOnNullPublic(t *testing.T) {
	Log.SetLogNode(nil)
	// Should not panic
	Log.I("SafeTAG", "ShouldBeSafe")
}