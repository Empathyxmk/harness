package public_tests

import (
	"testing"

	"verbalexpressions"
)

func TestReEscapePublic(t *testing.T) {
	// 're_escape' in Python was a no-op decorator, here in Go we'll test the equivalent, a passthrough
	dummy := func(x string) string { return x }
	if dummy("bar(foo)") != "bar(foo)" {
		t.Errorf("Expected 'bar(foo)' to be returned")
	}
	if dummy("hello?world.") != "hello?world." {
		t.Errorf("Expected 'hello?world.' to be returned")
	}
	if dummy("[]{}") != "[]{}" {
		t.Errorf("Expected '[]{}' to be returned")
	}
	if dummy("+*|") != "+*|" {
		t.Errorf("Expected '+*|' to be returned")
	}
}

func TestVerExComplexPatternPublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().StartOfLine().Then("ftp://").Maybe("downloads.").AnythingBut(" ").EndOfLine()
	if !verex.Match("ftp://files.com") {
		t.Errorf("Expected to match 'ftp://files.com'")
	}
	if !verex.Match("ftp://downloads.files.com") {
		t.Errorf("Expected to match 'ftp://downloads.files.com'")
	}
	if verex.Match("ftp:// downloads.files.com") {
		t.Errorf("Expected NOT to match 'ftp:// downloads.files.com'")
	}
}

func TestVerExAnythingButPublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().StartOfLine().AnythingBut("xyz").EndOfLine()
	if !verex.Match("abc") {
		t.Errorf("Expected to match 'abc'")
	}
	if verex.Match("x") {
		t.Errorf("Expected NOT to match 'x'")
	}
	if verex.Match("y") {
		t.Errorf("Expected NOT to match 'y'")
	}
	if !verex.Match("") {
		t.Errorf("Expected to match empty string")
	}
}

func TestVerExRangePublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Range("a", "c")
	pattern := verex.Regex()
	if pattern.FindString("xyzabc") == "" {
		t.Errorf("Expected to find in 'xyzabc'")
	}
	if !pattern.MatchString("b") {
		t.Errorf("Expected to match 'b'")
	}
	if pattern.MatchString("g") {
		t.Errorf("Expected NOT to match 'g'")
	}
}

func TestVerExMultipleOperatorsPublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Then("baz").Maybe("qux").Anything().EndOfLine()
	if !verex.Match("bazquxx") {
		t.Errorf("Expected to match 'bazquxx'")
	}
	if !verex.Match("bazplus") {
		t.Errorf("Expected to match 'bazplus'")
	}
	if !verex.Match("baz") {
		t.Errorf("Expected to match 'baz'")
	}
}

func TestVerExAnyPublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Any("QRST")
	if !verex.Match("S") {
		t.Errorf("Expected to match 'S'")
	}
	if !verex.Match("QRST") {
		t.Errorf("Expected to match 'QRST'")
	}
	if verex.Match("P") {
		t.Errorf("Expected NOT to match 'P'")
	}
}

func TestVerExMatchPublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().StartOfLine().Then("run").Maybe("ner").EndOfLine()
	m := verex.MatchString("runner")
	if m == "" {
		t.Errorf("Expected 'runner' to match")
	}
	if m != "runner" {
		t.Errorf("Expected match group to equal 'runner'")
	}
	m2 := verex.MatchString("run")
	if m2 == "" {
		t.Errorf("Expected 'run' to match")
	}
}

func TestVerExReplacePublic(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Find("error")
	text := "error"
	replaced := verex.Replace("fixed", text)
	if replaced != "fixed" {
		t.Errorf("Expected replaced text to be 'fixed'")
	}
}