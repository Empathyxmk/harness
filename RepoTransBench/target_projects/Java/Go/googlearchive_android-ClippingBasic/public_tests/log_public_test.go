package public_tests

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

func TestSetAndGetLogNodePublic(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	if getLogNode() != node {
		t.Errorf("Expected log node to be set and gotten back")
	}
}

func TestPrintlnWithThrowablePublic(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	tr := errors.New("PublicException")
	myLog.Println(tests.ERROR, "PUB", "public_msg", tr)
	if node.Priority != tests.ERROR || node.Tag != "PUB" || node.Msg != "public_msg" || node.Tr != tr {
		t.Error("Println failed to pass correct arguments with throwable (Public)")
	}
}

func TestPrintlnWithoutThrowablePublic(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	myLog.Println(tests.WARN, "PUB2", "public_msg2", nil)
	if node.Priority != tests.WARN || node.Tag != "PUB2" || node.Msg != "public_msg2" || node.Tr != nil {
		t.Error("Println failed to pass correct arguments without throwable (Public)")
	}
}

func TestLevelShortcutsPublic(t *testing.T) {
	node := &TestLogNode{}
	setLogNode(node)
	tests.V("PUBv", "visible")
	if node.Priority != tests.VERBOSE {
		t.Error("Expected VERBOSE priority (Public)")
	}
	tests.D("PUBd", "debugging")
	if node.Priority != tests.DEBUG {
		t.Error("Expected DEBUG priority (Public)")
	}
	tests.I("PUBi", "information")
	if node.Priority != tests.INFO {
		t.Error("Expected INFO priority (Public)")
	}
	tests.W("PUBw", "warning")
	if node.Priority != tests.WARN {
		t.Error("Expected WARN priority (Public)")
	}
	tests.E("PUBe", "error occurred", errors.New("ise"))
	if node.Priority != tests.ERROR {
		t.Error("Expected ERROR priority (Public)")
	}
	tests.WTF("PUBa", "assertion")
	if node.Priority != tests.ASSERT {
		t.Error("Expected ASSERT priority (Public)")
	}
}

func TestNoLogNodeSetPublic(t *testing.T) {
	setLogNode(nil)
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Should not panic when log node is nil (Public)")
		}
	}()
	myLog.Println(tests.INFO, "PUB", "public_msg", nil)
}