package original

import (
	"testing"
)

func TestInnerClass(t *testing.T) {
	outer := &OuterClass{42}
	inner := outer.NewInner()
	if got := inner.addOuterField(8); got != 50 {
		t.Errorf("Expected 50, got %d", got)
	}
}

func TestInnerClassWithProtectedField(t *testing.T) {
	outer := &InnerClassWithProtectedField{77}
	inner := outer.NewInnerWithProtected()
	if got := inner.multiplyOuterField(2); got != 154 {
		t.Errorf("Expected 154, got %d", got)
	}
}

type OuterClass struct {
	value int
}
func (o *OuterClass) NewInner() *OuterClassInner {
	return &OuterClassInner{o}
}
type OuterClassInner struct {
	outer *OuterClass
}
func (i *OuterClassInner) addOuterField(by int) int {
	return i.outer.value + by
}

type InnerClassWithProtectedField struct {
	value int
}
func (o *InnerClassWithProtectedField) NewInnerWithProtected() *InnerWithProtectedField {
	return &InnerWithProtectedField{o}
}
type InnerWithProtectedField struct {
	outer *InnerClassWithProtectedField
}
func (i *InnerWithProtectedField) multiplyOuterField(by int) int {
	return i.outer.value * by
}