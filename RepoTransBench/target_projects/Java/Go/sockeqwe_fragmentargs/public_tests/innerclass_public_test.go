package public_tests

import (
	"testing"
)

func TestInnerClassAccessPublicVariant(t *testing.T) {
	outer := &OuterClassPublic{21}
	inner := outer.NewInner()
	if got := inner.multiplyOuterField(5); got != 105 {
		t.Errorf("Expected 105, got %d", got)
	}
}

type OuterClassPublic struct {
	value int
}

func (o *OuterClassPublic) NewInner() *OuterClassInnerPublic {
	return &OuterClassInnerPublic{o}
}

type OuterClassInnerPublic struct {
	outer *OuterClassPublic
}

func (i *OuterClassInnerPublic) multiplyOuterField(by int) int {
	return i.outer.value * by
}