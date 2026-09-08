package original

import (
	"testing"
)

func TestInjectorInterfaceShouldAllowAnyObject(t *testing.T) {
	inj := &anyObjectInjector{}
	inj.Inject("dummy")
}

type anyObjectInjector struct{}

func (a *anyObjectInjector) Inject(target interface{}) {
	// no-op, just check interface accepts any object
}