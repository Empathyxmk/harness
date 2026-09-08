package tests

import (
	"strings"
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestXPathExprStrAndAddCondition(t *testing.T) {
	x := cssselect.NewXPathExpr("//", "div", "foo=1")
	if got := x.String(); got != "//div[foo=1]" {
		t.Errorf("Got string: %q, want \"//div[foo=1]\"", got)
	}
	x.AddCondition("bar=2")
	if strings.Contains(x.Condition, "[foo=1)") {
		t.Error("parentheses are wrapped incorrectly")
	}
	if !strings.Contains(x.Condition, "bar=2") {
		t.Error("Condition missing bar=2 after add")
	}
}

func TestXPathExprAddNameTest(t *testing.T) {
	x := cssselect.NewXPathExpr("//", "div", "")
	x.AddNameTest()
	if x.Element != "*" {
		t.Errorf("Expected element '*', got: %v", x.Element)
	}
	if !strings.Contains(x.Condition, "name()") {
		t.Error("Condition missing name() after add_name_test")
	}
}

func TestXPathExprAddStarPrefix(t *testing.T) {
	x := cssselect.NewXPathExpr("//", "*", "")
	x.AddStarPrefix()
	if !(x.Path == "//*" || strings.HasSuffix(x.Path, "*/")) {
		t.Errorf("Expected path to end with '*/' or be '//*', got: %q", x.Path)
	}
}

func TestXPathExprJoin(t *testing.T) {
	x1 := cssselect.NewXPathExpr("//", "a", "foo=1")
	x2 := cssselect.NewXPathExpr("/*/", "span", "bar=2")
	r := x1.Join("|", x2, "::", true)
	if r == nil {
		t.Fatal("Join returned nil")
	}
	if !strings.HasPrefix(r.Element, "span") {
		t.Errorf("result element does not start with 'span': %v", r.Element)
	}
	if !strings.Contains(r.Path, "|") {
		t.Errorf("Path missing '|': %v", r.Path)
	}
}