package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"skydoves/preferenceroom/tests"
)

type InjectorGenerator struct {
	pcac           *tests.Mock
	injectedName   string
	elementUtils   *tests.Mock
}

func (ig *InjectorGenerator) generate() *tests.TypeSpec {
	return &tests.TypeSpec{
		Name: ig.injectedName + "_Injector",
		Body: "func() { /* contains PreferenceRoom */ }",
	}
}

func TestGenerateClassName(t *testing.T) {
	pcac := tests.NewMock()
	elementUtils := tests.NewMock()

	// Simulate TypeElement's getSimpleName()
	injectedName := "MyClass"
	ig := InjectorGenerator{pcac, injectedName, elementUtils}
	spec := ig.generate()

	assert.Equal(t, "MyClass_Injector", spec.Name, "Class name should be {SimpleName}_Injector")
	assert.Contains(t, spec.Body, "PreferenceRoom")
}