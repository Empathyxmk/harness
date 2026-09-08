package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ModulePlain struct{}
type ModulePlainStub struct{}
type ModuleFooModule struct{}
type ModuleFooOverrideModule struct{}

type ModuleFeather struct {
	override bool
}

func (f *ModuleFeather) Instance(t string) interface{} {
	switch t {
	case "Plain":
		if f.override {
			return &ModulePlainStub{}
		}
		return &ModulePlain{}
	case "string":
		if f.override {
			return "bar"
		}
		return "foo"
	default:
		return nil
	}
}

func TestDependencyOverriddenByModule(t *testing.T) {
	feather := &ModuleFeather{override: true}
	plain := feather.Instance("Plain")
	assert.IsType(t, &ModulePlainStub{}, plain)
}

func TestModuleOverwrittenBySubClass(t *testing.T) {
	featherA := &ModuleFeather{}
	resultA := featherA.Instance("string")
	assert.Equal(t, "foo", resultA)

	featherB := &ModuleFeather{override: true}
	resultB := featherB.Instance("string")
	assert.Equal(t, "bar", resultB)
}