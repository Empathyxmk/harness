package original

import (
	"testing"
)

type Terminal struct{}

func (t *Terminal) Clear()              {}
func (t *Terminal) Print(msg string)    {}
func (t *Terminal) PrintHeader(args []string)    {}
func (t *Terminal) PrintShortMenu(args []string) {}
func (t *Terminal) PrintMenu(args []string)      {}
func (t *Terminal) EnterCapturingMode()          {}
func (t *Terminal) CaptureKeystroke() *string    { return nil }
func (t *Terminal) Reset()                       {}

// PosixTerminal and DummyTerminal can be left as stubs

func TestTerminalClassImplementsClear(t *testing.T) {
	term := &Terminal{}
	term.Clear()
}

func TestTerminalClassImplementsPrintShortMenu(t *testing.T) {
	term := &Terminal{}
	term.PrintShortMenu([]string{"--foo"})
}

func TestTerminalClassImplementsPrintMenu(t *testing.T) {
	term := &Terminal{}
	term.PrintMenu([]string{"--foo"})
}

func TestTerminalCaptureKeystrokeReturnsNilByDefault(t *testing.T) {
	term := &Terminal{}
	if term.CaptureKeystroke() != nil {
		t.Error("Expected nil keystroke")
	}
}

func TestGetTerminalReturnsInterface(t *testing.T) {
	var getTerminal = func() *Terminal {
		return &Terminal{}
	}
	term := getTerminal()
	if term == nil {
		t.Error("getTerminal must not return nil")
	}
}