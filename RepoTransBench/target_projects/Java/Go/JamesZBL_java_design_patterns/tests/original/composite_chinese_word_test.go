package original

import (
	"testing"
	"bytes"
	"os"
	"jameszbl_java_design_patterns/composite"
)

func TestChineseWordConstructorAndPrintBefore(t *testing.T) {
	c := composite.NewCharacter('中')
	word := composite.NewChineseWord([]*composite.Character{c})
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
	if got := string(result); got != "" {
		t.Errorf("word.PrintBefore() = '%s', want ''", got)
	}
}