package tests

import (
	"testing"
)

// Mocks for SelectCreator ported for testing allocation
type SelectCreator struct {
	paramIdx int
}

func (sc *SelectCreator) allocateParameter() string {
	idx := sc.paramIdx
	sc.paramIdx++
	return "param" + itoa(idx)
}

func itoa(n int) string {
	return fmt.Sprintf("%d", n)
}

func TestAbstractSqlCreator_AllocateParameter(t *testing.T) {
	sc := &SelectCreator{}
	if got := sc.allocateParameter(); got != "param0" {
		t.Errorf("expected param0, got %v", got)
	}
	if got := sc.allocateParameter(); got != "param1" {
		t.Errorf("expected param1, got %v", got)
	}
	if got := sc.allocateParameter(); got != "param2" {
		t.Errorf("expected param2, got %v", got)
	}
}