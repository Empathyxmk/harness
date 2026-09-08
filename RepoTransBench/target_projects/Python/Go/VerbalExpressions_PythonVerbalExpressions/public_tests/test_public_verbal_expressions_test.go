package public_tests

import (
	"testing"

	"verbalexpressions"
)

// Helper for full match
func isFullMatch(verex *verbalexpressions.VerEx, s string) bool {
	m := verex.MatchString(s)
	return m == s
}

func TestPublicStartOfLine(t *testing.T) {
	verex := verbalexpressions.NewVerEx().StartOfLine().Then("Begin")
	s := "BeginAgain"
	notS := "NotBegin"
	if !verex.Match(s) {
		t.Errorf("Expected to match 'BeginAgain'")
	}
	if verex.Match(notS) {
		t.Errorf("Expected NOT to match 'NotBegin'")
	}
}

func TestPublicAnything(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Anything()
	if !verex.Match("Some string") {
		t.Errorf("Expected to match 'Some string'")
	}
	if !verex.Match("") {
		t.Errorf("Expected to match ''")
	}
}

func TestPublicAnythingBut(t *testing.T) {
	verex := verbalexpressions.NewVerEx().AnythingBut("xyz")
	if !verex.Match("Hello world") {
		t.Errorf("Expected to match 'Hello world'")
	}
	m := verex.MatchString("xyzworld")
	if m != "" {
		t.Errorf("Expected empty group for 'xyzworld', got '%s'", m)
	}
}

func TestPublicEndOfLine(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Find("complete").EndOfLine()
	if !verex.Search("mission complete") {
		t.Errorf("Expected to find 'complete' at end of 'mission complete'")
	}
	if verex.Match("completely done") {
		t.Errorf("Expected NOT to match 'completely done'")
	}
}

func TestPublicMaybe(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Then("red").Maybe("car")
	if !isFullMatch(verex, "red") {
		t.Errorf("Expected to match 'red' (fullmatch)")
	}
	if !isFullMatch(verex, "redcar") {
		t.Errorf("Expected to match 'redcar' (fullmatch)")
	}
	if isFullMatch(verex, "redcars") {
		t.Errorf("Expected NOT to fullmatch 'redcars'")
	}
}

func TestPublicAnyOf(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Any("wxyz")
	if !verex.Match("z") {
		t.Errorf("Expected to match 'z'")
	}
	if !verex.Match("yell") {
		t.Errorf("Expected to match 'yell'")
	}
	if verex.Match("k") {
		t.Errorf("Expected NOT to match 'k'")
	}
}

func TestPublicNotOf(t *testing.T) {
	verex := verbalexpressions.NewVerEx().AnythingBut("LMN")
	if !verex.Match("abcde") {
		t.Errorf("Expected to match 'abcde'")
	}
	m := verex.MatchString("MMM")
	if m != "" {
		t.Errorf("Expected empty group for 'MMM', got '%s'", m)
	}
}

func TestPublicReplace(t *testing.T) {
	verex := verbalexpressions.NewVerEx().Find("swap_me")
	text := "swap_me"
	result := verex.Replace("changed", text)
	if result != "changed" {
		t.Errorf("Expected replaced text to be 'changed'")
	}
}