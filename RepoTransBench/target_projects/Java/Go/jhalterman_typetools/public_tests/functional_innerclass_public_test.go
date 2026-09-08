package public_tests

import (
	"reflect"
	"testing"
)

type OuterPublic[A any] struct{}

type InnerSet struct {
	OuterPublic[int]
}
type InnerHashSet struct {
	OuterPublic[int]
}

func TestResolveRawArgumentForInnerSet(t *testing.T) {
	tp := reflect.TypeOf(InnerSet{})
	if tp.Kind() != reflect.Struct {
		t.Errorf("Expected InnerSet to be struct")
	}
}

func TestResolveRawArgumentForInnerHashSet(t *testing.T) {
	tp := reflect.TypeOf(InnerHashSet{})
	if tp.Kind() != reflect.Struct {
		t.Errorf("Expected InnerHashSet to be struct")
	}
}