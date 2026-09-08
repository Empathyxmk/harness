package original

import (
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

// --- Mocks and Stubs ---

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

// Test UI widgets (stub)
type TextViewStub struct {
	text string
}

type ScrollViewStub struct{}

func (t *TextViewStub) SetText(s string) {
	t.text = s
}

// --- MainActivity static methods ---

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
		// do something for flashing
	}
}

func (m *MainActivity) onCreateOptionsMenu(menu interface{}) bool { return true }

func (m *MainActivity) onOptionsItemSelected(item *MenuItemStub) bool {
	if item.id == 1 { // about
		return true
	}
	if item.id == 2 { // flash_new
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

// fileWorker only for signature, not used in tests.
type fileWorker interface{}

// static runWithFilePath for the class
func RunWithFilePath(act interface{}, w fileWorker) {}

// --- TESTS ---

func TestMainActivity_AppendLog_DEBUG(t *testing.T) {
	DEBUG = true
	act := &MainActivity{}
	_appendLog("hello", act)
	appendLog("anything", act)
	DEBUG = false
}

func TestMainActivity_AppendLog_UI_Print(t *testing.T) {
	act := &MainActivity{
		logView:    &TextViewStub{},
		scrollView: &ScrollViewStub{},
	}
	appendLog("ui_print this is message", act)
	assert.Equal(t, "ui_print this is message", act.logView.text)
}

func TestMainActivity_FlashNew_NotFlashing(t *testing.T) {
	cur_status = StatusNormal
	act := &MainActivity{
		logView:    &TextViewStub{},
		scrollView: &ScrollViewStub{},
	}
	// These calls are stubs, so just verify they execute.
	act.flash_new()
}

func TestMainActivity_OnBackPressed_FlashingAndOther(t *testing.T) {
	act := &MainActivity{}
	cur_status = StatusNormal
	act.superOnBackPressed()
	act.onBackPressed()
	cur_status = StatusFlashing
	act.onBackPressed()
}

func TestMainActivity_OnCreateOptionsMenu(t *testing.T) {
	act := &MainActivity{}
	menu := struct{}{}
	ok := act.onCreateOptionsMenu(menu)
	assert.True(t, ok)
}

func TestMainActivity_OnOptionsItemSelected_about(t *testing.T) {
	act := &MainActivity{}
	item := &MenuItemStub{id: 1}
	assert.True(t, act.onOptionsItemSelected(item))
}

func TestMainActivity_OnOptionsItemSelected_flash_new(t *testing.T) {
	act := &MainActivity{}
	item := &MenuItemStub{id: 2}
	assert.True(t, act.onOptionsItemSelected(item))
}

func TestMainActivity_RunWithFilePath(t *testing.T) {
	RunWithFilePath(&MainActivity{}, nil)
}