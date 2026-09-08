package original

import (
	"reflect"
	"testing"
)

type FragmentArgsInjector interface {
	Inject(target interface{})
}

type FragmentArgs struct{}

var autoMappingInjector FragmentArgsInjector

func (FragmentArgs) inject(target interface{}) {
	if autoMappingInjector != nil {
		autoMappingInjector.Inject(target)
	}
}

func (FragmentArgs) injectFromBundle(target interface{}) {
	// Simulate autoMappingInjector lookup that may fail
	// For coverage: leave as is
}

func TestInjectWithNoAutoMappingClass(t *testing.T) {
	// Should not panic even if injector cannot be found.
	fa := FragmentArgs{}
	fa.inject(struct{}{})
}

type dummyInjector struct {
	injected bool
}

func (d *dummyInjector) Inject(target interface{}) {
	d.injected = true
}

func TestInjectWithAutoMappingInjectorPresent(t *testing.T) {
	// Reflection hack: simulate static field set
	var dummy = &dummyInjector{}
	autoMappingInjector = dummy

	fragment := struct{}{}
	FragmentArgs{}.inject(fragment)
	if !dummy.injected {
		t.Errorf("inject did not call DummyInjector.Inject")
	}

	// Clean up for other tests
	autoMappingInjector = nil
}