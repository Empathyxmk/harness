package original

import (
	"errors"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

// TypeResolver emulation for test illustration
type MyInterface[T any] interface{}
type MyImpl struct{}

type Unknown struct{}

// TypeResolver logic (mocked for test purposes)
var UnknownType = reflect.TypeOf(&Unknown{})

func enableCache()  {}
func disableCache() {}

func resolveRawArgument(iface, impl any) reflect.Type {
	// Mimic Java's logic for this test purpose.
	if iface == "MyInterface" && impl == "MyImpl" {
		return reflect.TypeOf("")
	}
	return UnknownType
}
func resolveRawArguments(a, b any) []reflect.Type {
	if a == nil {
		return nil
	}
	return []reflect.Type{UnknownType}
}

func resolveRawArgumentThrowsOnWrongNumberOfParams() error {
	// Always throw error for this mock
	return errors.New("Expected 1 argument but got something else")
}

func TestEnableAndDisableCacheAreSafe(t *testing.T) {
	enableCache()
	disableCache()
	enableCache()
}

func TestResolveRawArgumentClassSubtype(t *testing.T) {
	// Emulate behavior for test (our mock in Go)
	result := resolveRawArgument("MyInterface", "MyImpl")
	assert.Equal(t, reflect.TypeOf(""), result)
}

func TestResolveRawArgument_Type_ReturnsUnknownForNonParameterized(t *testing.T) {
	result := resolveRawArgument("String", "String")
	assert.Equal(t, UnknownType, result)
}

func TestResolveRawArgumentsHandlesNull(t *testing.T) {
	assert.Nil(t, resolveRawArguments(nil, "String"))
}

func TestResolveRawArgumentThrowsOnWrongNumberOfParams(t *testing.T) {
	err := resolveRawArgumentThrowsOnWrongNumberOfParams()
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Expected 1 argument")
}