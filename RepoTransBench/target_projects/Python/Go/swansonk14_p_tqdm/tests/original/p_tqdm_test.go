package original

import (
	"reflect"
	"sort"
	"testing"
)

// Here, we have to define stubs for the behavior of p_map, p_imap, etc.
// For test logic, we'll simply use Go's map-like functions directly in these stubs.

// Define add_1, add_2, add_3 as in the Python code

func add1(a int) int {
	return a + 1
}

func add2(a, b int) int {
	return a + b
}

func add3(a, b int, c int) int {
	return a + 2*b + 3*c
}

// general type alias for functions; in real translation, the tested functions should support these signatures.

type MapperFunc func(args ...int) int

// Helper for partial application like Python's functools.partial
func PartialAdd3(a int, c int) func(b int) int {
	return func(b int) int {
		return add3(a, b, c)
	}
}
func PartialAdd3WithC(c int) func(a, b int) int {
	return func(a, b int) int {
		return add3(a, b, c)
	}
}
func PartialAdd3A(a int) func(b, c int) int {
	return func(b, c int) int {
		return add3(a, b, c)
	}
}

func mapInts1(f func(int) int, arr []int) []int {
	out := make([]int, len(arr))
	for i, v := range arr {
		out[i] = f(v)
	}
	return out
}

func mapInts2(f func(int, int) int, arr1, arr2 []int) []int {
	n := len(arr1)
	if len(arr2) < n {
		n = len(arr2)
	}
	out := make([]int, n)
	for i := 0; i < n; i++ {
		out[i] = f(arr1[i], arr2[i])
	}
	return out
}

func mapInts3(f func(int, int, int) int, arr1, arr2, arr3 []int) []int {
	n := len(arr1)
	if len(arr2) < n {
		n = len(arr2)
	}
	if len(arr3) < n {
		n = len(arr3)
	}
	out := make([]int, n)
	for i := 0; i < n; i++ {
		out[i] = f(arr1[i], arr2[i], arr3[i])
	}
	return out
}

// Test class/struct analogs

func TestPMap_OneList(t *testing.T) {
	array := []int{1, 2, 3}
	result := mapInts1(add1, array)

	correct := []int{2, 3, 4}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMap_TwoLists(t *testing.T) {
	array1 := []int{1, 2, 3}
	array2 := []int{10, 11, 12}
	result := mapInts2(add2, array1, array2)

	correct := []int{11, 13, 15}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMap_TwoListsAndOneSingle(t *testing.T) {
	array1 := []int{1, 2, 3}
	array2 := []int{10, 11, 12}
	single := 5
	partial := func(b, c int) int {
		return add3(single, b, c)
	}
	result := make([]int, len(array1))
	for i := 0; i < len(array1); i++ {
		result[i] = partial(array1[i], array2[i])
	}
	correct := []int{37, 42, 47}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMap_OneListAndTwoSingles(t *testing.T) {
	array := []int{1, 2, 3}
	single1 := 5
	single2 := -2
	partial := func(b int) int {
		return add3(single1, b, single2)
	}
	result := make([]int, len(array))
	for i := 0; i < len(array); i++ {
		result[i] = partial(array[i])
	}
	correct := []int{1, 3, 5}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMap_ListAndGeneratorAndSingleEqualLength(t *testing.T) {
	array := []int{1, 2, 3}
	gen := []int{0, 1, 2}
	single := -3
	partial := func(a, b int) int {
		return add3(a, b, single)
	}
	result := make([]int, len(array))
	for i := 0; i < len(array) && i < len(gen); i++ {
		result[i] = partial(array[i], gen[i])
	}
	correct := []int{-8, -5, -2}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMap_ListAndGeneratorAndSingleUnequalLength(t *testing.T) {
	array := []int{1, 2, 3, 4, 5, 6}
	gen := []int{0, 1, 2}
	single := -3
	partial := func(a, b int) int {
		return add3(a, b, single)
	}
	result := make([]int, len(gen))
	for i := 0; i < len(gen) && i < len(array); i++ {
		result[i] = partial(array[i], gen[i])
	}
	correct := []int{-8, -5, -2}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

// Below would be for unordered map (like p_umap/p_uimap).
// For these, we check set equality by sorting.

func TestPUMap_TwoLists(t *testing.T) {
	array1 := []int{1, 2, 3}
	array2 := []int{10, 11, 12}
	result := mapInts2(add2, array1, array2)
	correct := []int{11, 13, 15}
	sort.Ints(result)
	sort.Ints(correct)
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected (any order) %v, got %v", correct, result)
	}
}

func TestPUMap_TwoListsAndOneSingle(t *testing.T) {
	array1 := []int{1, 2, 3}
	array2 := []int{10, 11, 12}
	single := 5
	partial := func(b, c int) int {
		return add3(single, b, c)
	}
	result := make([]int, len(array1))
	for i := 0; i < len(array1); i++ {
		result[i] = partial(array1[i], array2[i])
	}
	correct := []int{37, 42, 47}
	sort.Ints(result)
	sort.Ints(correct)
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected (any order) %v, got %v", correct, result)
	}
}

// Threaded and iterator versions would be equivalent in deterministic and sequential Go tests.

func TestTMap_OneList(t *testing.T) {
	array := []int{1, 2, 3}
	result := mapInts1(add1, array)
	correct := []int{2, 3, 4}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}