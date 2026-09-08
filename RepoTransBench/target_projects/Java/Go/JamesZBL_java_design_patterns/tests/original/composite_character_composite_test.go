package original

import (
	"bytes"
	"testing"

	"jameszbl_java_design_patterns/composite"
)

// Translated from: composite/src/test/java/me/zbl/composite/CharacterCompositeTest.java
func TestCharacterCompositeAddAndCount(t *testing.T) {
	composite := composite.NewCharacterComposite()
	if composite.Count() != 0 {
		t.Errorf("expected count 0, got %v", composite.Count())
	}
	composite.Add(composite.NewCharacterComposite())
	if composite.Count() != 1 {
		t.Errorf("expected count 1, got %v", composite.Count())
	}
}

func TestCharacterCompositePrintNoChildren(t *testing.T) {
	composite := composite.NewCharacterComposite()
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("print with no children panicked: %v", r)
		}
	}()
	composite.Print()
}

func TestCharacterCompositePrintBeforeAfterHooks(t *testing.T) {
	type TestComposite struct {
		composite.CharacterComposite
		beforeCalled bool
		afterCalled  bool
	}
	var tc TestComposite
	tc.CharacterComposite = *composite.NewCharacterCompositeWithHooks(
		func() { tc.beforeCalled = true }, func() { tc.afterCalled = true },
	)
	tc.Print()
	if !tc.beforeCalled {
		t.Errorf("before hook not called")
	}
	if !tc.afterCalled {
		t.Errorf("after hook not called")
	}
}

func TestCharacterCompositePrintDeepComposition(t *testing.T) {
	var sb bytes.Buffer
	comp := composite.NewCharacterCompositeWithHooks(
		func() { sb.WriteByte('[') },
		func() { sb.WriteByte(']') },
	)
	child := composite.NewCharacterCompositeWithHooks(
		func() { sb.WriteByte('A') },
		nil,
	)
	comp.Add(child)
	comp.Print()
	if got, want := sb.String(), "[A]"; got != want {
		t.Errorf("expected '%s', got '%s'", want, got)
	}
}