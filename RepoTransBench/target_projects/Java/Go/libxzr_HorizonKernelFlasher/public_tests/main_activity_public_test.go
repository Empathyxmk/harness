package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// -- Stubs and fakes reused/adapted from original test --

// Enum and types for fake UI logic
type MainActivity struct {
	logView    *TextViewStub
	scrollView *ScrollViewStub
}

type statusEnum int

const (
	StatusNormal statusEnum = iota
	StatusFlashing
	StatusError
)

var DEBUG bool
var cur_status statusEnum

type TextViewStub struct {
	text string
}
type ScrollViewStub struct{}

func (t *TextViewStub) SetText(s string) { t.text = s }

func _appendLog(msg string, act *MainActivity) {
	if DEBUG {
		return
	}
}

func appendLog(msg string, act *MainActivity) {
	if len(msg) > 0 && len(msg) >= 7 && msg[:7] == "ui_print" {
		if act != nil && act.logView != nil {
			act.logView.SetText(msg)
		}
	}
}

func (m *MainActivity) update_title()  {}
func (m *MainActivity) flash_new()     { m.update_title(); m.runWithFilePath(nil, nil) }
func (m *MainActivity) runWithFilePath(arg1 interface{}, arg2 interface{}) {}

func (m *MainActivity) onBackPressed() {
	if cur_status == StatusNormal {
		// would call super.OnBackPressed()
	} else {
		// do something for flashing or error
	}
}

func (m *MainActivity) onCreateOptionsMenu(menu interface{}) bool { return true }

func (m *MainActivity) onOptionsItemSelected(item *MenuItemStub) bool {
	if item.id == 3 { // help
		return true
	}
	if item.id == -12345 { // unknown
		m.flash_new()
		return true
	}
	return true
}

func (m *MainActivity) getAlertDialogBuilder() interface{} { return NewAlertDialogBuilder() }
func (m *MainActivity) getMenuInflater() interface{}       { return nil }

func (m *MainActivity) superOnBackPressed() {}

type MenuItemStub struct {
	id int
}

type AlertDialogBuilderStub struct{}

func NewAlertDialogBuilder() *AlertDialogBuilderStub {
	return &AlertDialogBuilderStub{}
}

type fileWorker interface{}

// -- Tests --

func TestMainActivityPublic_AppendLog_DEBUG(t *testing.T) {
	DEBUG = true
	act := &MainActivity{}
	_appendLog("world", act)
	appendLog("foobar", act)
	DEBUG = false
}

func TestMainActivityPublic_AppendLog_UI_Print(t *testing.T) {
	act := &MainActivity{
		logView:    &TextViewStub{},
		scrollView: &ScrollViewStub{},
	}
	appendLog("ui_print log with different msg", act)
	assert.Equal(t, "ui_print log with different msg", act.logView.text)
}

func TestMainActivityPublic_FlashNew_NotFlashing(t *testing.T) {
	cur_status = StatusNormal
	act := &MainActivity{
		logView:    &TextViewStub{},
		scrollView: &ScrollViewStub{},
	}
	act.flash_new()
}

func TestMainActivityPublic_OnBackPressed_FlashingAndOther(t *testing.T) {
	act := &MainActivity{}
	cur_status = StatusNormal
	act.superOnBackPressed()
	act.onBackPressed()
	cur_status = StatusError
	act.onBackPressed()
}

func TestMainActivityPublic_OnCreateOptionsMenu(t *testing.T) {
	act := &MainActivity{}
	menu := struct{}{}
	assert.True(t, act.onCreateOptionsMenu(menu))
}

func TestMainActivityPublic_OnOptionsItemSelected_about(t *testing.T) {
	act := &MainActivity{}
	item := &MenuItemStub{id: 3}
	assert.True(t, act.onOptionsItemSelected(item))
}

func TestMainActivityPublic_OnOptionsItemSelected_flash_new(t *testing.T) {
	act := &MainActivity{}
	item := &MenuItemStub{id: -12345}
	assert.True(t, act.onOptionsItemSelected(item))
}

func TestMainActivityPublic_RunWithFilePath(t *testing.T) {
	// The public test class uses a different fake worker type and Activity.
	act := &MainActivity{}
	// Only signature tested
	act.runWithFilePath(nil, nil)
}