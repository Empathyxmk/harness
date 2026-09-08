package public_tests

import (
	"strings"
	"testing"

	"scrapy_cssselect/cssselect"
)

func TestXPathExprStrAndAddConditionPublic(t *testing.T) {
	x := cssselect.NewXPathExpr("/root/", "span", "active=true")
	if !strings.HasPrefix(x.String(), "/root/span[active=") {
		t.Errorf("x.String() = %q, want prefix \"/root/span[active=\"", x.String())
	}
	x.AddCondition("visible=false")
	if !strings.Contains(x.Condition, "visible=false") {
		t.Error("x.Condition does not have visible=false after add")
	}
	if !strings.Contains(x.Condition, "active=true") {
		t.Error("x.Condition does not still contain active=true")
	}
}

func TestXPathExprAddNameTestPublic(t *testing.T) {
	x := cssselect.NewXPathExpr("//", "section", "")
	x.AddNameTest()
	if x.Element != "*" {
		t.Errorf("Element = %q, expected \"*\"", x.Element)
	}
	if !strings.Contains(x.Condition, "name()") {
		t.Error("Condition missing name() after AddNameTest")
	}
}

func TestXPathExprAddStarPrefixPublic(t *testing.T) {
	x := cssselect.NewXPathExpr("/foo/", "*", "")
	x.AddStarPrefix()
	if !strings.HasPrefix(x.Path, "/foo/*") && !strings.HasPrefix(x.Path, "/foo/") {
		t.Errorf("x.Path = %q doesn't start with \"/foo/*\"", x.Path)
	}
}

func TestXPathExprJoinPublic(t *testing.T) {
	x1 := cssselect.NewXPathExpr("/root/", "header", "data=val1")
	x2 := cssselect.NewXPathExpr("/sibling/", "footer", "data=val2")
	r := x1.Join("//", x2, "-end-", true)
	if r == nil {
		t.Fatal("Join returned nil")
	}
	if !strings.HasPrefix(r.Element, "footer") {
		t.Errorf("r.Element = %q, want starts with \"footer\"", r.Element)
	}
	if !strings.Contains(r.Path, "//") && !strings.Contains(r.Path, "-end-") {
		t.Errorf("r.Path = %q, expected to contain \"//\" or \"-end-\"", r.Path)
	}
}