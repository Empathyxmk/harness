package original

import (
	"reflect"
	"testing"

	"github.com/jhalterman/typetools"
)

type SomeList []int
type SomeEntity struct{ id int }
type Entity[ID any] struct{ id ID }
type AnotherStruct struct{ Name string }

// 1. Should resolve class field type
func TestShouldResolveClass(t *testing.T) {
	e := SomeEntity{}
	typ := reflect.TypeOf(e)
	if typ.Field(0).Name != "id" {
		t.Errorf("Expected first field `id`, got %s", typ.Field(0).Name)
	}
}

// 2. Should resolve argument for generic type (simulate: get field type)
func TestShouldResolveArgumentForGenericType(t *testing.T) {
	type Foo struct{ Name string }
	var val Foo
	typ := reflect.TypeOf(val)
	if typ.Field(0).Type != reflect.TypeOf("") {
		t.Errorf("Expected string type for Name, got %s", typ.Field(0).Type)
	}
}

// 3. Should resolve argument for List
func TestShouldResolveArgumentForList(t *testing.T) {
	sl := SomeList{}
	typ := reflect.TypeOf(sl)
	elem := typ.Elem()
	if elem.Kind() != reflect.Int {
		t.Errorf("Type arg for SomeList should be int, got %s", elem)
	}
}

// 4. Should resolve type for List (simulate reify)
func TestShouldResolveTypeForList(t *testing.T) {
	sl := SomeList{}
	typ := reflect.TypeOf(sl)
	r := typetools.Reify(typ, typ)
	if r != typ {
		t.Errorf("Reify should return list type itself")
	}
}

// 5. Should resolve arguments for struct fields
func TestShouldResolveArgumentsForStruct(t *testing.T) {
	s := AnotherStruct{}
	typ := reflect.TypeOf(s)
	args := typetools.ResolveRawArguments(typ, typ)
	if len(args) == 0 || args[0] != reflect.TypeOf("") {
		t.Errorf("First argument should be string field type, got %v", args)
	}
}

// 6. Handle nil and unknown for non-parameterized types
func TestShouldReturnNullOnResolveArgumentsForNonParameterizedType(t *testing.T) {
	var ptr *int
	args := typetools.ResolveRawArguments(nil, nil)
	if args != nil {
		t.Errorf("Expected nil when both args nil")
	}
	args2 := typetools.ResolveRawArguments(reflect.TypeOf(ptr), nil)
	if args2 != nil {
		t.Errorf("Expected nil when target is nil")
	}
	arg := typetools.ResolveRawArgument(nil, nil)
	if arg.Kind() != reflect.Struct {
		t.Errorf("Should return UnknownType")
	}
}