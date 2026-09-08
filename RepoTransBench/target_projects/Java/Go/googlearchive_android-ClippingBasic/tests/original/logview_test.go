package original

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

// Simulates 'runOnUiThread'
func (d *DummyActivity) RunOnUiThread(f func()) {
	d.DidRunOnUiThread = true
	d.LastRunnable = f
	f()
}

// LogView is constructed with a pointer to DidRunOnUiThread for emulation
func TestAppendIfNotNullBehavior(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)

	sb := ""
	value := "abc"
	res := view.AppendIfNotNull(&sb, &value, ",")
	if *res != "abc," {
		t.Errorf("Expected 'abc,', got '%s'", *res)
	}

	sb = ""
	var nilVal *string
	res = view.AppendIfNotNull(&sb, nilVal, "|")
	if *res != "" {
		t.Errorf("Expected empty string, got '%s'", *res)
	}

	sb = "x"
	emptyStr := ""
	res = view.AppendIfNotNull(&sb, &emptyStr, "|")
	if *res != "x" {
		t.Errorf("Expected 'x', got '%s'", *res)
	}
}

func TestGetSetNext(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)
	filter := &tests.MessageOnlyLogFilter{}
	view.SetNext(filter)
	if view.GetNext() != filter {
		t.Errorf("Expected next to be filter")
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

func TestPrintlnFormatsAndRunsRunnable(t *testing.T) {
	uiEmu := false
	view := tests.NewLogView(&uiEmu)
	mockNode := &MockLogNode{}
	view.SetNext(mockNode)

	err := &customErr{msg: "e"}
	view.Println(tests.INFO, "tag", "msg", err)
	if !mockNode.Called {
		t.Errorf("Expected next LogNode to be called")
	}
	if !uiEmu {
		t.Errorf("Expected runOnUiThread emulation")
	}
}

type customErr struct{ msg string }
func (c *customErr) Error() string { return c.msg }