package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
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

// Format utils
func formatList(list []string) string {
	if len(list) == 0 {
		return ""
	}
	res := ""
	for i, v := range list {
		if i > 0 {
			res += "\n"
		}
		res += "  " + v
	}
	return res
}

func formatMissing(a, b []string, nameA, nameB string) string {
	var res string
	if len(a) > 0 {
		res += "missing from " + nameA + ":\n"
		for _, v := range a {
			res += "  " + v + "\n"
		}
	}
	if len(b) > 0 {
		res += "missing from " + nameB + ":\n"
		for _, v := range b {
			res += "  " + v + "\n"
		}
	}
	if len(res) > 0 && res[len(res)-1] == '\n' {
		res = res[:len(res)-1]
	}
	return res
}

type Failure struct {
	msg string
}

func NewFailure(msg string) *Failure {
	return &Failure{msg: msg}
}
func (f *Failure) Error() string  { return f.msg }
func (f *Failure) String() string { return f.msg }

type CommandFailed struct {
	cmd   []string
	code  int
	error string
}

func NewCommandFailed(cmd []string, code int, errmsg string) *CommandFailed {
	return &CommandFailed{cmd, code, errmsg}
}
func (c *CommandFailed) Error() string {
	return "command " + c.cmd[0] + " failed"
}
func (c *CommandFailed) String() string {
	return "command " + c.cmd[0] + " failed: " + c.error
}

func TestUI_QuietAndVerbose(t *testing.T) {
	ui := NewUI(0)
	assert.True(t, ui.quiet)
	assert.False(t, ui.verbose)

	ui = NewUI(2)
	assert.False(t, ui.quiet)
	assert.True(t, ui.verbose)
}

func TestUI_InfoMethods(t *testing.T) {
	ui := NewUI(2)
	ui.info("info message")
	ui.infoBegin("begin message")
	ui.infoContinue("continued...")
	ui.infoEnd("done!")
	ui.setToBeContinued(true)
	ui.info("info after tbc")
	ui.error("error message")
	ui.warning("warn message")
}

func TestUI_InfoQuiet(t *testing.T) {
	ui := NewUI(0)
	ui.info("nothing prints")
	ui.infoBegin("nothing prints begin")
	ui.infoContinue("nothing prints continue")
	ui.infoEnd("nothing prints end")
}

func TestUI_ErrorAndWarning(t *testing.T) {
	ui := NewUI(1)
	ui.error("E")
	ui.warning("W")
}

func TestFormatList(t *testing.T) {
	assert.Equal(t, "", formatList([]string{}))
	assert.Equal(t, "  a\n  b", formatList([]string{"a", "b"}))
}

func TestFormatMissing(t *testing.T) {
	assert.Equal(t, "", formatMissing([]string{}, []string{}, "A", "B"))
	assert.Equal(t, "missing from A:\n  one", formatMissing([]string{"one"}, []string{}, "A", "B"))
	assert.Equal(t, "missing from B:\n  two", formatMissing([]string{}, []string{"two"}, "A", "B"))
	val := formatMissing([]string{"x"}, []string{"y"}, "A", "B")
	assert.Contains(t, val, "missing from A")
	assert.Contains(t, val, "missing from B")
}

func TestFailure_Message(t *testing.T) {
	msg := "fail msg"
	f := NewFailure(msg)
	assert.Equal(t, msg, f.String())
}

func TestCommandFailed(t *testing.T) {
	c := NewCommandFailed([]string{"cmd"}, 1, "nope")
	assert.Contains(t, c.String(), "failed")
}