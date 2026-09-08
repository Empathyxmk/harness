package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Translation of ToggleExpandLayoutTest from Java

type testListener struct {
	startOpen   int
	startClose  int
	onOpen      int
	onClosed    int
}

func (t *testListener) OnStartOpen(h, oh int) { t.startOpen++ }
func (t *testListener) OnOpen()               { t.onOpen++ }
func (t *testListener) OnStartClose(h, oh int) { t.startClose++ }
func (t *testListener) OnClosed()              { t.onClosed++ }

func TestToggleExpandLayout_SetOnToggleTouchListener(t *testing.T) {
	layout := NewToggleExpandLayout(&Context{})
	lis := &testListener{}
	layout.SetOnToggleTouchListener(lis)
	if assert.NotNil(t, layout) {
	}
}

func TestToggleExpandLayout_OpenAndCloseNoChildren(t *testing.T) {
	layout := NewToggleExpandLayout(&Context{})
	lis := &testListener{}
	layout.SetOnToggleTouchListener(lis)

	layout.Open()
	layout.Close()
}

func TestToggleExpandLayout_OpenAndCloseWithChildren(t *testing.T) {
	layout := NewToggleExpandLayout(&Context{})
	child0 := NewMockView(20, 15)
	child1 := NewMockView(30, 10)
	layout.AddChild(child0)
	layout.AddChild(child1)
	lis := &testListener{}
	layout.SetOnToggleTouchListener(lis)
	layout.OnLayout(true, 0, 0, 30, 25)
	layout.Open()
	layout.Close()
	if lis.startOpen == 0 {
		t.Error("Listener OnStartOpen should be called at least once")
	}
	if lis.startClose == 0 {
		t.Error("Listener OnStartClose should be called at least once")
	}
}

func TestToggleExpandLayout_MultipleListeners(t *testing.T) {
	layout := NewToggleExpandLayout(&Context{})
	lis1 := &testListener{}
	lis2 := &testListener{}
	layout.SetOnToggleTouchListener(lis1)
	layout.SetOnToggleTouchListener(lis2)

	layout.Open()
	layout.Close()
	// In Go, only the last set listener is kept, like Java's setXxxListener
	if lis1.startOpen != 0 {
		t.Error("First listener should not receive events after replaced")
	}
	if lis2.startOpen == 0 {
		t.Error("Second listener should receive events after being set")
	}
}