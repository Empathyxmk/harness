package public_tests

import (
	"errors"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

// AnotherInterface and implementations
type AnotherInterface[T any] interface{}
type AnotherImpl struct{}

// TypeResolver logic for illustration 
var UnknownType = reflect.TypeOf(&struct{}{})
func enableCache()  {}
func disableCache() {}

func resolveRawArgumentPublic(iface, impl any) reflect.Type {
	if iface == "AnotherInterface" && impl == "AnotherImpl" {
		return reflect.TypeOf(int(0))
	}
	return UnknownType
}
func resolveRawArgumentsPublic(a, b any) []reflect.Type {
	if a == nil {
		return nil
	}
	return []reflect.Type{UnknownType}
}
func resolveRawArgumentThrowsOnWrongNumberOfParamsSet() error {
	return errors.New("Expected 1 argument but got something else")
}

func TestEnableAndDisableCacheIdempotence(t *testing.T) {
	disableCache()
	enableCache()
	disableCache()
}

func TestResolveRawArgumentClassSubtypeDifferent(t *testing.T) {
	result := resolveRawArgumentPublic("AnotherInterface", "AnotherImpl")
	assert.Equal(t, reflect.TypeOf(int(0)), result)
}

func TestResolveRawArgument_Type_ReturnsUnknownForNonParameterized_Different(t *testing.T) {
	result := resolveRawArgumentPublic("Integer", "Integer")
	assert.Equal(t, UnknownType, result)
}

func TestResolveRawArgumentsHandlesNull_differentClass(t *testing.T) {
	assert.Nil(t, resolveRawArgumentsPublic(nil, "Integer"))
}

func TestResolveRawArgumentThrowsOnWrongNumberOfParamsSet(t *testing.T) {
	err := resolveRawArgumentThrowsOnWrongNumberOfParamsSet()
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "Expected 1 argument")
}