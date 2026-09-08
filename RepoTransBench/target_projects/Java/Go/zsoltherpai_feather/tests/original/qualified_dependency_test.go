package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type QualFoo interface{}

type QualFooA struct{}
type QualFooB struct{}

type QualifiedFeather struct{}

func (f *QualifiedFeather) Instance(key string) QualFoo {
	switch key {
	case "A":
		return &QualFooA{}
	case "B":
		return &QualFooB{}
	default:
		return nil
	}
}

// Dummy simulates constructor injection, DummyTestUnit simulates field injection
type QualDummy struct {
	Foo QualFoo
}

func (f *QualifiedFeather) InjectDummy(dummy *QualDummy, qual string) {
	dummy.Foo = f.Instance(qual)
}

type QualDummyTestUnit struct {
	Foo QualFoo
}

func (f *QualifiedFeather) InjectDummyTestUnit(dummy *QualDummyTestUnit, qual string) {
	dummy.Foo = f.Instance(qual)
}

func TestQualifiedInstances(t *testing.T) {
	feather := &QualifiedFeather{}
	assert.IsType(t, &QualFooA{}, feather.Instance("A"))
	assert.IsType(t, &QualFooB{}, feather.Instance("B"))
}

func TestInjectedQualified(t *testing.T) {
	feather := &QualifiedFeather{}
	dummy := &QualDummy{}
	feather.InjectDummy(dummy, "B")
	assert.IsType(t, &QualFooB{}, dummy.Foo)
}

func TestFieldInjectedQualified(t *testing.T) {
	feather := &QualifiedFeather{}
	dummy := &QualDummyTestUnit{}
	feather.InjectDummyTestUnit(dummy, "A")
	assert.IsType(t, &QualFooA{}, dummy.Foo)
}