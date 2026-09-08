package original

import (
	"reflect"
	"testing"
	"time"

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

func TestGeneratorYieldMultipleValues(t *testing.T) {
	input := []int{10, 20, 30}
	g := NewGenerator(func(yield func(int)) {
		for _, x := range input {
			yield(x)
		}
	})
	got := list(g.Iterator())
	if !reflect.DeepEqual(got, input) {
		t.Errorf("Expected %v, got %v", input, got)
	}
}

func TestGeneratorAlternatingTypes(t *testing.T) {
	type myStruct struct {
		A int
		B string
	}
	input := []myStruct{
		{1, "foo"},
		{2, "bar"},
	}
	g := NewGenerator(func(yield func(myStruct)) {
		for _, ms := range input {
			yield(ms)
		}
	})
	got := list(g.Iterator())
	if !reflect.DeepEqual(got, input) {
		t.Errorf("Expected %v, got %v", input, got)
	}
}

func TestGeneratorNoYield(t *testing.T) {
	g := NewGenerator[float64](func(yield func(float64)) {})
	got := list(g.Iterator())
	want := []float64{}
	if !reflect.DeepEqual(got, want) {
		t.Errorf("Expected empty slice, got %v", got)
	}
}

func TestGeneratorStopIteration(t *testing.T) {
	g := NewGenerator(func(yield func(int)) {
		yield(1)
		yield(2)
		// do not yield more
	})
	it := g.Iterator()
	if !it.HasNext() {
		t.Fatal("Expected HasNext() to be true")
	}
	if it.Next() != 1 {
		t.Error("Expected first value 1")
	}
	if !it.HasNext() {
		t.Fatal("Expected HasNext() to be true after first")
	}
	if it.Next() != 2 {
		t.Error("Expected second value 2")
	}
	if it.HasNext() {
		t.Fatal("Expected HasNext() to be false at end")
	}
}

func TestGeneratorConcurrency(t *testing.T) {
	g := NewGenerator(func(yield func(int)) {
		yield(1)
		time.Sleep(30 * time.Millisecond)
		yield(2)
	})
	iter := g.Iterator()
	values := []int{}
	for iter.HasNext() {
		values = append(values, iter.Next())
	}
	want := []int{1, 2}
	if !reflect.DeepEqual(values, want) {
		t.Errorf("Expected %v, got %v", want, values)
	}
}

func TestGeneratorReuseIterator(t *testing.T) {
	g := NewGenerator(func(yield func(string)) {
		yield("hello")
		yield("world")
	})
	it1 := g.Iterator()
	it2 := g.Iterator()
	v1 := list(it1)
	v2 := list(it2)
	want := []string{"hello", "world"}
	if !reflect.DeepEqual(v1, want) || !reflect.DeepEqual(v2, want) {
		t.Errorf("Iterator reuse: values not as expected. Got %v and %v, want %v", v1, v2, want)
	}
}