package public_tests

import (
	"testing"

	"jameszbl_java_design_patterns/composite"
)

func TestChineseWordWithOtherCharacters(t *testing.T) {
	c1 := composite.NewCharacter('我')
	c2 := composite.NewCharacter('们')
	word := composite.NewChineseWord([]*composite.Character{c1, c2})
	if word.Count() != 2 {
		t.Errorf("got count %d, want 2", word.Count())
	}
}