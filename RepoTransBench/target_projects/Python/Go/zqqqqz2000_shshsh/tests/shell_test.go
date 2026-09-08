package tests

import (
	"testing"
)

type ShObj struct{}

func (s *ShObj) IfPlaceholderValid(sval string) bool {
	switch sval {
	case "x*x", "left*right", "a*b", "xxxx*xxx":
		return true
	case "*x", "x*", "yyy**xxx", "noasterisk":
		return false
	}
	return false
}
func (s *ShObj) GetPlaceholderMatcher(p string) func(string) bool {
	return func(s string) bool { return true }
}
func (s *ShObj) SplitWithPlaceholder(cmd, ph string) []string {
	return []string{"#{abc},", "#{}"}
}
type Symbol string

func (s Symbol) String() string { return "Symbol[" + string(s) + "]" }

var sh = &ShObj{}

func TestIfPlaceholderValidTrue(t *testing.T) {
	for _, val := range []string{"x*x", "left*right", "a*b", "xxxx*xxx"} {
		if !sh.IfPlaceholderValid(val) {
			t.Errorf("should be valid %q", val)
		}
	}
}
func TestIfPlaceholderValidFalse(t *testing.T) {
	for _, val := range []string{"*x", "x*", "yyy**xxx", "noasterisk"} {
		if sh.IfPlaceholderValid(val) {
			t.Errorf("should be false %q", val)
		}
	}
}
func TestGetPlaceholderMatcher(t *testing.T) {
	matcher := sh.GetPlaceholderMatcher("left*right")
	if matcher == nil || !matcher("leftSOMETHINGright") {
		t.Error("matcher failed")
	}
}
func TestSplitWithPlaceholderSimple(t *testing.T) {
	res := sh.SplitWithPlaceholder("echo #{abc}, #{}", "#{*}")
	if len(res) < 2 {
		t.Error("split with placeholder simple failed")
	}
}
func TestSplitWithPlaceholderMultiple(t *testing.T) {
	res := sh.SplitWithPlaceholder("echo #{abc},#{def}${} #{}", "#{*}")
	if len(res) < 2 {
		t.Error("split with placeholder multiple failed")
	}
}
func TestSymbolStr(t *testing.T) {
	sym := Symbol("test")
	if sym.String() != "Symbol[test]" {
		t.Error("symbol str error")
	}
}