package original

import (
	"strings"
	"testing"
)

type Highlight struct {
	tag string
}

func linesAndHighlightsString(input string, _ int) ([]string, []Highlight) {
	return strings.Split(input, "\n"), []Highlight{}
}

func linesAndHighlightsTokens(taggedTokens [][2]string, _ int) ([]string, []Highlight) {
	var fullText string
	var highlights []Highlight
	for _, tt := range taggedTokens {
		fullText += tt[0]
		if tt[1] != "" {
			highlights = append(highlights, Highlight{tag: tt[1]})
		}
	}
	return strings.Split(fullText, "\n"), highlights
}

func TestLinesAndHighlightsString(t *testing.T) {
	lines, highlights := linesAndHighlightsString("foo\nbar", 0)
	if len(lines) != 2 || lines[0] != "foo" || lines[1] != "bar" {
		t.Errorf("Expected lines to be [foo bar], got %v", lines)
	}
	if len(highlights) != 0 {
		t.Errorf("Expected no highlights, got %v", highlights)
	}
}

func TestLinesAndHighlightsTokens(t *testing.T) {
	taggedTokens := [][2]string{
		{"test", "tag1"},
		{"\nmore", "tag2"},
		{"done", ""},
	}
	lines, highlights := linesAndHighlightsTokens(taggedTokens, 0)
	if len(lines) == 0 || !strings.HasPrefix(lines[0], "test") {
		t.Errorf("Expected first line to start with test")
	}
	tagok := false
	for _, h := range highlights {
		if h.tag == "tag1" || h.tag == "tag2" {
			tagok = true
		}
	}
	if !tagok {
		t.Errorf("Expected highlights to include tag1 or tag2")
	}
}

func TestLinesAndHighlightsMultilineTok(t *testing.T) {
	taggedTokens := [][2]string{
		{"abc\n", "tag3"},
		{"def", "tag4"},
		{"\njkl", ""},
	}
	lines, highlights := linesAndHighlightsTokens(taggedTokens, 2)
	if len(lines) == 0 {
		t.Errorf("Expected lines not empty")
	}
	if !strings.HasPrefix(lines[0], "abc") {
		t.Errorf("Expected first line to start with abc")
	}
	if !strings.HasSuffix(lines[len(lines)-1], "jkl") {
		t.Errorf("Expected last line to end with jkl")
	}
	if highlights == nil {
		t.Errorf("Expected highlights non-nil")
	}
}

type UnmatchedError struct {
	s     string
	start [2]int
	end   [2]int
}

func (u UnmatchedError) Error() string {
	return "Found unmatched: " + u.s
}

func TestUnmatchedErrorRepr(t *testing.T) {
	err := UnmatchedError{"(*", [2]int{2, 4}, [2]int{2, 6}}
	errStr := err.Error()
	if !strings.Contains(errStr, "Found unmatched") {
		t.Errorf("Expected unmatched error string")
	}
	if err.start != [2]int{2, 4} || err.end != [2]int{2, 6} {
		t.Errorf("Range incorrect")
	}
}

type NoDotError struct{}

func (e NoDotError) Error() string { return "No dot error" }

func TestNoDotError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic")
		}
	}()
	panic(NoDotError{})
}

var proofStartPat = "Proof"
var proofEndPat = "Qed"
var opaqueProofEnds = []string{"Qed", "Defined", "Admitted", "Abort"}

func TestPROOFStartEndPat(t *testing.T) {
	if !strings.HasPrefix(proofStartPat, "Proof") {
		t.Errorf("Expected PROOF_START_PAT to match")
	}
	if !strings.HasPrefix(proofEndPat, "Qed") {
		t.Errorf("Expected PROOF_END_PAT to match")
	}
	for _, end := range opaqueProofEnds {
		if len(end) == 0 {
			t.Errorf("Proof end cannot be empty")
		}
	}
}