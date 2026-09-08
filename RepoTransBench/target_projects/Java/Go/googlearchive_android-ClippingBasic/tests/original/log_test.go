package original

import (
	"errors"
	"testing"

	"clippingbasic/tests"
)

type TestLogNode struct {
	Priority int
	Tag      string
	Msg      string
	Tr       error
}

func (n *TestLogNode) Println(priority int, tag, msg string, tr error) {
	n.Priority = priority
	n.Tag = tag
	n.Msg = msg
	n.Tr = tr
}

var myLog = &tests.Log{}

func setLogNode(node tests.LogNode) {
	myLog.SetLogNode(node)
}

func getLogNode() tests.LogNode {
	return myLog.GetLogNode()
}

func TestSetAndGetLogNode(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	if getLogNode() != node {
		t.Errorf("Expected log node to be set and gotten back")
	}
}

func TestPrintlnWithThrowable(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	tr := errors.New("Exception")
	myLog.Println(tests.DEBUG, "TAG", "msg", tr)
	if node.Priority != tests.DEBUG || node.Tag != "TAG" || node.Msg != "msg" || node.Tr != tr {
		t.Error("Println failed to pass correct arguments with throwable")
	}
}

func TestPrintlnWithoutThrowable(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	myLog.Println(tests.INFO, "TAG2", "msg2", nil)
	if node.Priority != tests.INFO || node.Tag != "TAG2" || node.Msg != "msg2" || node.Tr != nil {
		t.Error("Println failed to pass correct arguments without throwable")
	}
}

func TestLevelShortcuts(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)

	tests.V("TAGv", "verbose")
	if node.Priority != tests.VERBOSE {
		t.Error("Expected VERBOSE priority")
	}
	tests.D("TAGd", "debug")
	if node.Priority != tests.DEBUG {
		t.Error("Expected DEBUG priority")
	}
	tests.I("TAGi", "info")
	if node.Priority != tests.INFO {
		t.Error("Expected INFO priority")
	}
	tests.W("TAGw", "warn")
	if node.Priority != tests.WARN {
		t.Error("Expected WARN priority")
	}
	tests.E("TAGe", "error", errors.New("npe"))
	if node.Priority != tests.ERROR {
		t.Error("Expected ERROR priority")
	}
	tests.WTF("TAGa", "assert")
	if node.Priority != tests.ASSERT {
		t.Error("Expected ASSERT priority")
	}
}

func TestNoLogNodeSet(t *testing.T) {
	setLogNode(nil)
	// Just ensure calling doesn't panic if node is nil
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Should not panic when log node is nil")
		}
	}()
	myLog.Println(tests.DEBUG, "TAG", "msg", nil)
}