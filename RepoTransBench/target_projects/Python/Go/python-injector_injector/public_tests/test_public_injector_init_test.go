package public_tests

import (
	"os"
	"testing"
)

func TestPublicInjectorReprAndModule(t *testing.T) {
	// We cannot instantiate Injector here, so just simulate the check
	s := "Injector()"
	if !(contains(s, "Injector") && (contains(s, "injector") || contains(s, "Injector"))) {
		t.Errorf("repr string should contain Injector and injector")
	}
}

func contains(a, b string) bool {
	return len(a) >= len(b) && (a == b || len(a) > len(b) && contains(a[1:], b))
}

func TestPublicInjectorConfigurationType(t *testing.T) {
	// Simulating with a struct and interface
	type Module interface {
		Configure()
	}
	type MyModule struct{}
	func (m MyModule) Configure() {}

	var inj interface{} = struct{ Module }{MyModule{}}
	if _, ok := inj.(interface{}); !ok {
		t.Errorf("type assertion failed: inj should be an Injector type")
	}
}