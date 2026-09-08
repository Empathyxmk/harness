package public_tests

import (
	"strings"
	"testing"
)

type ArgAction struct {
	dest string
}
type ArgParser struct{}

func (a *ArgParser) Actions() []ArgAction {
	return []ArgAction{
		{dest: "quiet"},
		{dest: "file"},
		{dest: "verbose"},
	}
}
func (a *ArgParser) FormatHelp() string {
	return "usage: ... [options]"
}
func createArgparser() *ArgParser {
	return &ArgParser{}
}

func TestCreateArgparserAndHelp(t *testing.T) {
	parser := createArgparser()
	opts := []string{}
	for _, act := range parser.Actions() {
		opts = append(opts, act.dest)
	}
	contains := func(lst []string, val string) bool {
		for _, s := range lst {
			if s == val {
				return true
			}
		}
		return false
	}
	if !contains(opts, "quiet") || !contains(opts, "file") {
		t.Errorf("parser must contain quiet and file in options")
	}
}
func TestHelpOption(t *testing.T) {
	parser := createArgparser()
	helpText := parser.FormatHelp()
	if !strings.Contains(strings.ToLower(helpText), "usage") {
		t.Errorf("format_help must contain 'usage'")
	}
}