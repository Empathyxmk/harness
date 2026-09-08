package original

import (
	"bytes"
	"os"
	"strings"
	"testing"
	"jameszbl_java_design_patterns/composite"
)

func TestEnglishSentenceConstructorAndPrintAfter(t *testing.T) {
	word := composite.NewEnglishWord([]*composite.Character{})
	sentence := composite.NewEnglishSentence([]*composite.EnglishWord{word})
	if got := sentence.Count(); got != 1 {
		t.Errorf("sentence.Count() = %d, want 1", got)
	}
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	os.Stdout = w
	sentence.PrintAfter()
	w.Close()
	os.Stdout = os.Stdout
	// Platform EOL
	result, _ := io.ReadAll(r)
	want := ".\n"
	got := strings.ReplaceAll(string(result), "\r\n", "\n")
	if got != want {
		t.Errorf("PrintAfter() = %q, want %q", got, want)
	}
}