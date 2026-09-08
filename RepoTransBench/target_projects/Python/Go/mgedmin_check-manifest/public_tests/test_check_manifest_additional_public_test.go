package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	// Assume check_manifest is implemented with needed types and functions for Go tests
	// "mgedmin_check_manifest/check_manifest"
)

type UI struct {
	verbosity      int
	quiet          bool
	verbose        bool
	_toBeContinued bool
}

func NewUI(verbosity int) *UI {
	quiet := verbosity <= 0
	verbose := verbosity > 1
	return &UI{
		verbosity:      verbosity,
		quiet:          quiet,
		verbose:        verbose,
		_toBeContinued: false,
	}
}

func (u *UI) info(_ string)           {}
func (u *UI) infoBegin(_ string)      {}
func (u *UI) infoContinue(_ string)   {}
func (u *UI) infoEnd(_ string)        {}
func (u *UI) error(_ string)          {}
func (u *UI) warning(_ string)        {}
func (u *UI) setToBeContinued(val bool) { u._toBeContinued = val }

func formatList(items []string) string {
	if len(items) == 0 {
		return ""
	}
	result := ""
	for i, item := range items {
		if i > 0 {
			result += "\n"
		}
		result += "  " + item
	}
	return result
}

func formatMissing(a, b []string, nameA, nameB string) string {
	s := ""
	if len(a) > 0 {
		s += "missing from " + nameA + ":\n"
		for _, v := range a {
			s += "  " + v + "\n"
		}
	}
	if len(b) > 0 {
		s += "missing from " + nameB + ":\n"
		for _, v := range b {
			s += "  " + v + "\n"
		}
	}
	// Remove trailing newline if exists
	if len(s) > 0 && s[len(s)-1] == '\n' {
		s = s[:len(s)-1]
	}
	return s
}

type Failure struct {
	msg string
}

func NewFailure(msg string) *Failure {
	return &Failure{msg: msg}
}
func (f *Failure) Error() string { return f.msg }
func (f *Failure) String() string { return f.msg }

type CommandFailed struct {
	cmd   []string
	code  int
	error string
}

func NewCommandFailed(cmd []string, code int, errorMsg string) *CommandFailed {
	return &CommandFailed{cmd, code, errorMsg}
}
func (c *CommandFailed) Error() string {
	return "command " + c.cmd[0] + " failed with code"
}
func (c *CommandFailed) String() string {
	return "command " + c.cmd[0] + " failed: " + c.error
}

// ---- Test Suite ----
func TestUI_Public_QuietAndVerbose(t *testing.T) {
	ui := NewUI(1)
	assert.False(t, ui.quiet)
	assert.False(t, ui.verbose)

	ui = NewUI(3)
	assert.False(t, ui.quiet)
	assert.True(t, ui.verbose)
}

func TestUI_Public_InfoMethods(t *testing.T) {
	ui := NewUI(3)
	ui.info("public info message")
	ui.infoBegin("public begin message")
	ui.infoContinue("public continued...")
	ui.infoEnd("public done!")
	ui.setToBeContinued(true)
	ui.info("public info after tbc")
	ui.error("public error message")
	ui.warning("public warn message")
}

func TestUI_Public_InfoQuiet(t *testing.T) {
	ui := NewUI(-1)
	ui.info("nothing to print here")
	ui.infoBegin("still nothing begin")
	ui.infoContinue("still nothing continue")
	ui.infoEnd("still nothing end")
}

func TestUI_Public_ErrorAndWarning(t *testing.T) {
	ui := NewUI(1)
	ui.error("ERROR for public")
	ui.warning("WARNING for public")
}

func TestFormatList_Public(t *testing.T) {
	assert.Equal(t, "  x", formatList([]string{"x"}))
	assert.Equal(t, "  foo\n  bar\n  baz", formatList([]string{"foo", "bar", "baz"}))
}

func TestFormatMissing_Public(t *testing.T) {
	assert.Equal(
		t,
		"missing from Alpha:\n  first\nmissing from Beta:\n  second",
		formatMissing([]string{"first"}, []string{"second"}, "Alpha", "Beta"),
	)
	assert.Equal(
		t,
		"missing from Dst:\n  hello",
		formatMissing([]string{}, []string{"hello"}, "Src", "Dst"),
	)
	assert.Equal(
		t,
		"missing from Src:\n  world",
		formatMissing([]string{"world"}, []string{}, "Src", "Dst"),
	)
	assert.Equal(t, "", formatMissing([]string{}, []string{}, "One", "Two"))
}

func TestFailure_Public_Message(t *testing.T) {
	msg := "another fail message"
	f := NewFailure(msg)
	assert.Equal(t, msg, f.String())
}

func TestCommandFailed_Public(t *testing.T) {
	c := NewCommandFailed([]string{"echo", "abc"}, 99, "fatal error")
	str := c.String()
	assert.Contains(t, str, "failed")
	assert.Contains(t, str, "echo")
}