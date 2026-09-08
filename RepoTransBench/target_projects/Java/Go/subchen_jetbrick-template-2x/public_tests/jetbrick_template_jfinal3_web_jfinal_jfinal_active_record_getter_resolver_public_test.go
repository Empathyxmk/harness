package public_tests

import (
	"testing"
)

type DummyClass struct {
	dummyVal int
}

func TestDummyGetter(t *testing.T) {
	obj := DummyClass{dummyVal: 99}
	if obj.dummyVal != 99 {
		t.Errorf("Dummy getter logic failed: got %d, expected 99", obj.dummyVal)
	}
}