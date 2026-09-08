package public_tests

import (
	"testing"

	"clippingbasic/tests"
)

type DummyActivity struct {
	DidRunOnUiThread bool
	LastRunnable     func()
}

func NewDummyActivity() *DummyActivity {
	return &DummyActivity{}
}

func (d *DummyActivity) RunOnUiThread(f func()) {
	d.DidRunOnUiThread = true
	d.LastRunnable = f
	f()
}

func TestAppendIfNotNullPublic(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)

	sb := ""
	value := "xyz"
	res := view.AppendIfNotNull(&sb, &value, ";")
	if *res != "xyz;" {
		t.Errorf("Expected 'xyz;', got '%s'", *res)
	}

	sb = ""
	var nilVal *string
	res = view.AppendIfNotNull(&sb, nilVal, "~")
	if *res != "" {
		t.Errorf("Expected empty string, got '%s'", *res)
	}

	sb = "y"
	emptyStr := ""
	res = view.AppendIfNotNull(&sb, &emptyStr, "?")
	if *res != "y" {
		t.Errorf("Expected 'y', got '%s'", *res)
	}
}

func TestGetSetNextPublic(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)
	filter := &tests.MessageOnlyLogFilter{}
	view.SetNext(filter)
	if view.GetNext() != filter {
		t.Errorf("Expected next to be filter (Public)")
	}
}

type MockLogNode struct {
	Called      bool
	CallParams  []interface{}
}

func (n *MockLogNode) Println(priority int, tag, msg string, tr error) {
	n.Called = true
	n.CallParams = []interface{}{priority, tag, msg, tr}
}

func TestPrintlnFormatsAndRunsRunnablePublic(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)
	mockNode := &MockLogNode{}
	view.SetNext(mockNode)

	err := &customErr{msg: "pubTest"}
	view.Println(tests.WARN, "publicTag", "publicMsg", err)
	if !mockNode.Called {
		t.Errorf("Expected next LogNode to be called (Public)")
	}
	if !uiEmu {
		t.Errorf("Expected runOnUiThread emulation (Public)")
	}
}

type customErr struct{ msg string }
func (c *customErr) Error() string { return c.msg }