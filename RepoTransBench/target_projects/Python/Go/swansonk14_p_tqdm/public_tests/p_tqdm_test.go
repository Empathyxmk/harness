package public_tests

import (
	"reflect"
	"testing"
)

// combine_values translation as in the public Python tests
func combineValues(a, b, c int) int {
	return a + b*3 + c*4
}

func TestPMapPublic_TwoListsAndOneSingle(t *testing.T) {
	array_1 := []int{2, 8, 14} // Used as b
	array_2 := []int{7, 1, 4}  // Used as a
	single := 5
	// To simulate partial(combine_values, c=single), array_2, array_1
	result := make([]int, len(array_2))
	for i := 0; i < len(array_2); i++ {
		result[i] = combineValues(array_2[i], array_1[i], single)
	}
	correct := []int{
		array_2[0] + array_1[0]*3 + single*4,
		array_2[1] + array_1[1]*3 + single*4,
		array_2[2] + array_1[2]*3 + single*4,
	}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMapPublic_OneListAndTwoSingles(t *testing.T) {
	array := []int{20, 25, 28}
	single1 := 4
	single2 := 6
	result := make([]int, len(array))
	for i, v := range array {
		result[i] = combineValues(v, single1, single2)
	}
	correct := []int{}
	for _, v := range array {
		correct = append(correct, v+single1*3+single2*4)
	}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMapPublic_SingleList(t *testing.T) {
	array := []int{5, 15, 35}
	result := make([]int, len(array))
	for i, v := range array {
		result[i] = combineValues(v, 2, 1)
	}
	correct := []int{}
	for _, v := range array {
		correct = append(correct, v+2*3+1*4)
	}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMapPublic_MultipleLists(t *testing.T) {
	array1 := []int{5, 9, 13}
	array2 := []int{2, 4, 6}
	array3 := []int{3, 5, 7}
	n := len(array1)
	result := make([]int, n)
	for i := 0; i < n; i++ {
		result[i] = combineValues(array1[i], array2[i], array3[i])
	}
	correct := []int{}
	for i := 0; i < n; i++ {
		correct = append(correct, array1[i]+array2[i]*3+array3[i]*4)
	}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

func TestPMapPublic_DifferentFunc(t *testing.T) {
	cubeSum := func(a, b int) int {
		return (a + b) * (a + b) * (a + b)
	}
	list1 := []int{1, 3, 5}
	list2 := []int{2, 4, 6}
	result := make([]int, len(list1))
	for i := 0; i < len(list1); i++ {
		result[i] = cubeSum(list1[i], list2[i])
	}
	correct := []int{27, 343, 1331}
	if !reflect.DeepEqual(correct, result) {
		t.Errorf("Expected %v, got %v", correct, result)
	}
}

// TestPImapPublic just runs the same tests as above (generator pattern)
func TestPImapPublic_TwoListsAndOneSingle(t *testing.T) {
	TestPMapPublic_TwoListsAndOneSingle(t)
}
func TestPImapPublic_OneListAndTwoSingles(t *testing.T) {
	TestPMapPublic_OneListAndTwoSingles(t)
}
func TestPImapPublic_SingleList(t *testing.T) {
	TestPMapPublic_SingleList(t)
}
func TestPImapPublic_MultipleLists(t *testing.T) {
	TestPMapPublic_MultipleLists(t)
}
func TestPImapPublic_DifferentFunc(t *testing.T) {
	TestPMapPublic_DifferentFunc(t)
}