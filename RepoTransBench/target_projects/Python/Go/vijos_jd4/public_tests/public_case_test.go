package public_tests

import (
	"strings"
	"testing"
)

type Case struct {
	name   string
	input  string
	output string
	score  int
}

func (c *Case) Name() string  { return c.name }
func (c *Case) Input() string { return c.input }
func (c *Case) Output() string { return c.output }
func (c *Case) Score() int    { return c.score }
func (c *Case) String() string {
	return c.name + " " + c.input + " " + c.output + " score=" + string(rune(c.score+'0'))
}

func TestCaseReprDiffParams(t *testing.T) {
	c := Case{"test_case2", "input-42", "output-99", 15}
	s := c.String()
	if !strings.Contains(s, "test_case2") || !strings.Contains(s, "score=15") {
		t.Errorf("repr does not contain right params: %s", s)
	}
}

func TestCasePropertiesDifferent(t *testing.T) {
	c := Case{"sampleB", "abc", "def", 8}
	if c.Name() != "sampleB" {
		t.Errorf("name mismatch")
	}
	if c.Input() != "abc" {
		t.Errorf("input mismatch")
	}
	if c.Output() != "def" {
		t.Errorf("output mismatch")
	}
	if c.Score() != 8 {
		t.Errorf("score mismatch")
	}
}

func TestCaseEqFalse(t *testing.T) {
	c := Case{"eqtest2", "in", "out", 1}
	var v interface{} = 42
	if c == v {
		t.Errorf("should not be equal to an int")
	}
}

func TestCaseOrderingDifferentName(t *testing.T) {
	c1 := Case{"case0002", "", "", 0}
	c2 := Case{"case0010", "", "", 0}
	if !(c1.name < c2.name) {
		t.Errorf("expected ordering case0002 < case0010")
	}
}

func TestCaseStrContent(t *testing.T) {
	c := Case{"visible2", "inputY", "outputY", 4}
	s := c.String()
	if !strings.Contains(s, "visible2") || !strings.Contains(s, "inputY") ||
		!strings.Contains(s, "outputY") || !strings.Contains(s, "score=4") {
		t.Errorf("String() did not join all correctly: %s", s)
	}
}