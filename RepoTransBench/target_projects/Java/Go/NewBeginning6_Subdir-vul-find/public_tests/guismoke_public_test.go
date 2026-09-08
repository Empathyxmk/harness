package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestGuiBasicInstantiationPublic(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Gui instantiation panicked: %v", r)
		}
	}()
	g := example.NewGui()
	if g == nil {
		t.Errorf("Gui is nil after instantiation")
	}
}