package original

import (
	"bytes"
	"os"
	"testing"
	"jameszbl_java_design_patterns/composite"
)

func TestEnglishWordConstructorAndPrintBefore(t *testing.T) {
	c := composite.NewCharacter('a')
	word := composite.NewEnglishWord([]*composite.Character{c})
	if got := word.Count(); got != 1 {
		t.Errorf("word.Count() = %d, want 1", got)
	}
	buf := &bytes.Buffer{}
	r, w, _ := os.Pipe()
	os.Stdout = w
	word.PrintBefore()
	w.Close()
	os.Stdout = os.Stdout
	result, _ := io.ReadAll(r)
	if got := string(result); got != " " {
		t.Errorf("word.PrintBefore() = '%s', want ' '", got)
	}
}