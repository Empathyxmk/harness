package public_tests

import (
	"bytes"
	"io"
	"os"
	"strings"
	"testing"

	"jameszbl_java_design_patterns/composite"
)

func TestEnglishSentenceCompositionPublic(t *testing.T) {
	word1 := composite.NewEnglishWord([]*composite.Character{
		composite.NewCharacter('T'), composite.NewCharacter('e'), composite.NewCharacter('s'), composite.NewCharacter('t'),
	})
	word2 := composite.NewEnglishWord([]*composite.Character{
		composite.NewCharacter('P'), composite.NewCharacter('u'), composite.NewCharacter('b'), composite.NewCharacter('l'), composite.NewCharacter('i'), composite.NewCharacter('c'),
	})
	s := composite.NewEnglishSentence([]*composite.EnglishWord{word1, word2})
	if s.Count() != 2 {
		t.Errorf("count: got %d, want 2", s.Count())
	}
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	old := os.Stdout
	os.Stdout = w
	s.Print()
	w.Close()
	os.Stdout = old
	result, _ := io.ReadAll(r)
	output := string(result)
	if !strings.Contains(output, ".") {
		t.Errorf("expected output to contain '.', got: %s", output)
	}
}