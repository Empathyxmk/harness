package public_tests

import (
	"testing"
)

// Simulate primitive dep injection, singleton, and provider reuse using Go idioms

type Alpha struct{}
type Beta struct{}
type Foo struct{}

// Singleton registry for this test
type Injector struct {
	alpha *Alpha
	beta  *Beta
	foo   *Foo
	intval int
}

func (inj *Injector) GetAlpha() *Alpha {
	if inj.alpha == nil {
		inj.alpha = &Alpha{}
	}
	return inj.alpha
}

func (inj *Injector) GetBeta() *Beta {
	if inj.beta == nil {
		inj.beta = &Beta{}
	}
	return inj.beta
}

func (inj *Injector) GetFoo() *Foo {
	if inj.foo == nil {
		inj.foo = &Foo{}
	}
	return inj.foo
}

func (inj *Injector) CallWithIntDep(f func(int) int) int {
	return f(inj.intval)
}

func TestPublicSingletonBindingUniqueValue(t *testing.T) {
	inj := &Injector{}
	a1 := inj.GetAlpha()
	b1 := inj.GetBeta()
	if a1 == nil {
		t.Errorf("expected a1 to be non-nil")
	}
	if b1 == nil {
		t.Errorf("expected b1 to be non-nil")
	}
	a2 := inj.GetAlpha()
	b2 := inj.GetBeta()
	if a1 != a2 {
		t.Errorf("Alpha values should be identical singleton")
	}
	if b1 != b2 {
		t.Errorf("Beta values should be identical singleton")
	}
}

func TestPublicInjectDecoratorWithPrimitive(t *testing.T) {
	inj := &Injector{intval: 77}
	provide := func(value int) int {
		return value
	}
	result := inj.CallWithIntDep(provide)
	if result != 77 {
		t.Errorf("expected result to be 77, got %d", result)
	}
}

func TestPublicProviderReuseTypes(t *testing.T) {
	inj := &Injector{}
	foo1 := inj.GetFoo()
	foo2 := inj.GetFoo()
	if foo1 != foo2 {
		t.Errorf("Foo object expected to be the same singleton instance, but got different ones")
	}
}