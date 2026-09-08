package public_tests

import (
	"testing"
)

type publicDoubleInjector struct{}

func (p *publicDoubleInjector) Inject(target interface{}) {
	// Accepts any target, checks for double (float64)
	if _, ok := target.(float64); ok {
		// no-op
	}
}

func TestInjectorInterfaceShouldAllowAnyObjectPublicTest(t *testing.T) {
	inj := &publicDoubleInjector{}
	inj.Inject(77.7) // pass double-type
}