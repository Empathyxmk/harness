package original

import (
	"errors"
	"reflect"
	"testing"
)

// Placeholder Log implementation for test translation.
type LogImp interface {
	V(tag, msg string, obj ...interface{})
	I(tag, msg string, obj ...interface{})
	W(tag, msg string, obj ...interface{})
	D(tag, msg string, obj ...interface{})
	E(tag, msg string, obj ...interface{})
	PrintErrStackTrace(tag string, tr error, format string, obj ...interface{})
}

type logManager struct {
	imp LogImp
}

var globalLog = &logManager{}

// Mimic static get/set
func SetLogImp(imp LogImp) {
	globalLog.imp = imp
}
func GetLogImp() LogImp {
	return globalLog.imp
}

// Delegate functions
func V(tag, msg string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.V(tag, msg, obj...)
	}
}
func I(tag, msg string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.I(tag, msg, obj...)
	}
}
func W(tag, msg string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.W(tag, msg, obj...)
	}
}
func D(tag, msg string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.D(tag, msg, obj...)
	}
}
func E(tag, msg string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.E(tag, msg, obj...)
	}
}
func PrintErrStackTrace(tag string, tr error, format string, obj ...interface{}) {
	if globalLog.imp != nil {
		globalLog.imp.PrintErrStackTrace(tag, tr, format, obj...)
	}
}

type TestLogImp struct {
	VC, IC, WC, DC, EC, PCS bool
	LastTag, LastMsg        string
	LastObj                 []interface{}
	LastTr                  error
	LastFormat              string
}

func (t *TestLogImp) V(tag, msg string, obj ...interface{}) {
	t.VC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *TestLogImp) I(tag, msg string, obj ...interface{}) {
	t.IC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *TestLogImp) W(tag, msg string, obj ...interface{}) {
	t.WC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *TestLogImp) D(tag, msg string, obj ...interface{}) {
	t.DC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *TestLogImp) E(tag, msg string, obj ...interface{}) {
	t.EC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *TestLogImp) PrintErrStackTrace(tag string, tr error, format string, obj ...interface{}) {
	t.PCS = true
	t.LastTag = tag
	t.LastTr = tr
	t.LastFormat = format
	t.LastObj = obj
}

var orig LogImp

func setup() {
	orig = GetLogImp()
}
func cleanup() {
	SetLogImp(orig)
}

func TestSetAndGetImpl(t *testing.T) {
	setup()
	defer cleanup()
	imp := &TestLogImp{}
	SetLogImp(imp)
	if GetLogImp() != imp {
		t.Error("SetLogImp or GetLogImp failed")
	}
}

func TestLogMethodsDelegateToImpl(t *testing.T) {
	setup()
	defer cleanup()
	imp := &TestLogImp{}
	SetLogImp(imp)

	V("TAG", "Ver msg %d", 1)
	I("TAG", "Info msg")
	W("TAG", "Warn %d", 42)
	D("TAG", "Dbg")
	E("TAG", "Err %s", "msg")
	tr := errors.New("err")
	PrintErrStackTrace("TAG", tr, "format %s", "err")

	if !imp.VC {
		t.Error("V not called")
	}
	if !imp.IC {
		t.Error("I not called")
	}
	if !imp.WC {
		t.Error("W not called")
	}
	if !imp.DC {
		t.Error("D not called")
	}
	if !imp.EC {
		t.Error("E not called")
	}
	if !imp.PCS {
		t.Error("PrintErrStackTrace not called")
	}
	if imp.LastTr != tr {
		t.Error("LastTr not set properly")
	}
	if imp.LastTag != "TAG" {
		t.Errorf("Expected TAG, got %s", imp.LastTag)
	}
}

func TestNullImplDoesNotThrow(t *testing.T) {
	SetLogImp(nil)
	// Should not panic
	V("TAG", "msg")
	D("TAG", "msg")
	I("TAG", "msg")
	W("TAG", "msg")
	E("TAG", "msg")
	PrintErrStackTrace("TAG", errors.New("err"), "msg")
}

func TestRefEq(t *testing.T) {
	a := &TestLogImp{}
	b := &TestLogImp{}
	if reflect.DeepEqual(a, b) && a != b {
		t.Error("TestLogImp struct should not be equal by reference")
	}
}