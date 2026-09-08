package public_tests

import (
	"errors"
	"testing"
)

// Copy of Log system for public test
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

// Public test log imp variant
type PublicTestLogImp struct {
	VC, IC, WC, DC, EC, PCS bool
	LastTag, LastMsg        string
	LastObj                 []interface{}
	LastTr                  error
	LastFormat              string
}

func (t *PublicTestLogImp) V(tag, msg string, obj ...interface{}) {
	t.VC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *PublicTestLogImp) I(tag, msg string, obj ...interface{}) {
	t.IC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *PublicTestLogImp) W(tag, msg string, obj ...interface{}) {
	t.WC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *PublicTestLogImp) D(tag, msg string, obj ...interface{}) {
	t.DC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *PublicTestLogImp) E(tag, msg string, obj ...interface{}) {
	t.EC = true
	t.LastTag = tag
	t.LastMsg = msg
	t.LastObj = obj
}
func (t *PublicTestLogImp) PrintErrStackTrace(tag string, tr error, format string, obj ...interface{}) {
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

func TestSetAndGetImplPublic(t *testing.T) {
	setup()
	defer cleanup()
	imp := &PublicTestLogImp{}
	SetLogImp(imp)
	if GetLogImp() != imp {
		t.Error("SetLogImp or GetLogImp failed")
	}
}

func TestLogMethodsDelegateToImplPublic(t *testing.T) {
	setup()
	defer cleanup()
	imp := &PublicTestLogImp{}
	SetLogImp(imp)

	V("PUB", "Verbose log %d", 10)
	I("PUB", "Info log")
	W("PUB", "Warning %d", 24)
	D("PUB", "Debug message")
	E("PUB", "Error string %s", "oops")
	tr := errors.New("public error")
	PrintErrStackTrace("PUB", tr, "formatting %s", "msg2")

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
	if imp.LastTag != "PUB" {
		t.Errorf("Expected PUB, got %s", imp.LastTag)
	}
}

func TestNullImplDoesNotThrowPublic(t *testing.T) {
	SetLogImp(nil)
	V("PUB", "message")
	D("PUB", "message")
	I("PUB", "message")
	W("PUB", "message")
	E("PUB", "message")
	PrintErrStackTrace("PUB", errors.New("public error"), "message")
}