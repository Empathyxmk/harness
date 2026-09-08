package public_tests

import (
	"reflect"
	"testing"

	. "github.com/example/mherrmann_go_generator_functions/generator"
)

// Helper: Drain the iterator into a slice
func list[T comparable](it *Iterator[T]) []T {
	var res []T
	for it.HasNext() {
		res = append(res, it.Next())
	}
	return res
}

func TestGeneratorEmpty(t *testing.T) {
	g := NewGenerator[any](func(yield func(any)) {})
	got := list(g.Iterator())
	want := []any{}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected %v, got %v", want, got)
	}
}

func TestGeneratorSingleElement(t *testing.T) {
	input := []int{42}
	g := NewGenerator(func(yield func(int)) {
		yield(42)
	})
	got := list(g.Iterator())
	if !reflect.DeepEqual(got, input) {
		t.Errorf("Expected %v, got %v", input, got)
	}
}

func TestGeneratorMultipleElements(t *testing.T) {
	input := []string{"foo", "bar", "baz"}
	g := NewGenerator(func(yield func(string)) {
		for _, s := range input {
			yield(s)
		}
	})
	got := list(g.Iterator())
	if !reflect.DeepEqual(got, input) {
		t.Errorf("Expected %v, got %v", input, got)
	}
}

func TestGeneratorEarlyExit(t *testing.T) {
	input := []int{1, 2, 3, 4, 5}
	g := NewGenerator(func(yield func(int)) {
		for _, v := range input {
			yield(v)
		}
	})
	iter := g.Iterator()
	got := []int{}
	for i := 0; i < 3 && iter.HasNext(); i++ {
		got = append(got, iter.Next())
	}
	want := []int{1, 2, 3}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected early exit got %v, want %v", got, want)
	}
}