package public

import (
	"testing"
)

// Simulate parameter allocation logic as per AbstractSqlCreatorPublicTest.java
type PublicSelectCreator struct {
	paramIdx int
}

func (sc *PublicSelectCreator) allocateParameter() string {
	s := "param" + itoa(sc.paramIdx)
	sc.paramIdx++
	return s
}

func TestAbstractSqlCreatorPublic_AllocateParameter(t *testing.T) {
	sc := &PublicSelectCreator{}
	got := sc.allocateParameter()
	if got != "param0" {
		t.Errorf("expected param0, got %v", got)
	}
	got = sc.allocateParameter()
	if got != "param1" {
		t.Errorf("expected param1, got %v", got)
	}
}