package public_tests

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

func TestGenerateDifferentClassName(t *testing.T) {
	pcac := tests.NewMock()
	elementUtils := tests.NewMock()
	injectedName := "PublicClass"
	ig := InjectorGenerator{pcac, injectedName, elementUtils}
	spec := ig.generate()
	assert.Equal(t, "PublicClass_Injector", spec.Name)
	assert.Contains(t, spec.Body, "PreferenceRoom")
}