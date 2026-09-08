package public_tests

import (
	"bytes"
	"testing"

	"jameszbl_java_design_patterns/composite"
)

func TestAddMultipleAndCountPublic(t *testing.T) {
	comp := composite.NewCharacterComposite()
	comp.Add(composite.NewCharacterComposite())
	comp.Add(composite.NewCharacterComposite())
	if comp.Count() != 2 {
		t.Errorf("expected count 2, got %d", comp.Count())
	}
}

func TestPrintNoChildrenPublic(t *testing.T) {
	comp := composite.NewCharacterComposite()
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("print with no children panicked: %v", r)
		}
	}()
	comp.Print()
}

func TestPrintBeforeAfterHooksPublic(t *testing.T) {
	beforeCalled := false
	afterCalled := false
	comp := composite.NewCharacterCompositeWithHooks(
		func() { beforeCalled = true },
		func() { afterCalled = true },
	)
	comp.Print()
	if !beforeCalled {
		t.Errorf("before hook not called")
	}
	if !afterCalled {
		t.Errorf("after hook not called")
	}
}

func TestPrintDeepCompositionPublic(t *testing.T) {
	var sb bytes.Buffer
	comp := composite.NewCharacterCompositeWithHooks(
		func() { sb.WriteByte('<') },
		func() { sb.WriteByte('>') },
	)
	child := composite.NewCharacterCompositeWithHooks(
		func() { sb.WriteByte('B') },
		nil,
	)
	comp.Add(child)
	comp.Print()
	if got := sb.String(); got != "<B>" {
		t.Errorf("expected '<B>', got %q", got)
	}
}