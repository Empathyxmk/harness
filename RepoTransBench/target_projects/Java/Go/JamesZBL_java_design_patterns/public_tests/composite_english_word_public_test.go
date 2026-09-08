package public_tests

import (
	"testing"

	"jameszbl_java_design_patterns/composite"
)

func TestEnglishWordConstructionAndPrintBeforeOtherValue(t *testing.T) {
	word := composite.NewEnglishWord([]*composite.Character{
		composite.NewCharacter('P'), composite.NewCharacter('u'), composite.NewCharacter('b'),
		composite.NewCharacter('l'), composite.NewCharacter('i'), composite.NewCharacter('c'),
	})
	if word.Count() != 6 {
		t.Errorf("got count %d, want 6", word.Count())
	}
	word.PrintBefore()
	// No output; just branch coverage
}