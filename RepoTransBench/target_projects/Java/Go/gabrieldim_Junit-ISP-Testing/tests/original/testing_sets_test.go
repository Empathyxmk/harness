package original

import (
	"testing"
	"sets"
)

func asSet(vals ...int) sets.IntSet {
	return sets.NewIntSet(vals...)
}

// Test: Both sets are neither empty nor nil; basic set difference with no overlap
func TestSetDifference_noOverlap_nonNull(t *testing.T) {
	set1 := asSet(1)
	set2 := asSet(2)
	result, err := sets.SetDifference(asSet(1), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result == nil {
		t.Fatalf("Expected non-nil result")
	}
	if !result.Equal(set1) {
		t.Errorf("Expected %v, got %v", set1, result)
	}
}

// Test: set2 is empty - set1 unchanged
func TestSetDifference_set2Empty(t *testing.T) {
	set1 := asSet(3)
	set2 := asSet()
	result, err := sets.SetDifference(asSet(3), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result == nil {
		t.Fatalf("Expected non-nil result")
	}
	if !result.Equal(set1) {
		t.Errorf("Expected %v, got %v", set1, result)
	}
}

// Test: set1 has elements, some overlap with set2
func TestSetDifference_withOverlap(t *testing.T) {
	set1 := asSet(1, 2, 3)
	set2 := asSet(2, 4)
	expected := asSet(1, 3)
	result, err := sets.SetDifference(asSet(1, 2, 3), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

// Test: set1 empty, set2 non-empty
func TestSetDifference_set1Empty_set2NonEmpty(t *testing.T) {
	set1 := asSet()
	set2 := asSet(4)
	result, err := sets.SetDifference(asSet(), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Test: set1 is nil
func TestSetDifference_set1Nil(t *testing.T) {
	set2 := asSet(1)
	_, err := sets.SetDifference(nil, set2)
	if err == nil {
		t.Fatalf("Expected error for nil set1, got nil")
	}
}

// Test: set2 is nil
func TestSetDifference_set2Nil(t *testing.T) {
	set1 := asSet(2)
	_, err := sets.SetDifference(set1, nil)
	if err == nil {
		t.Fatalf("Expected error for nil set2, got nil")
	}
}

// Test: both sets are nil
func TestSetDifference_bothNil(t *testing.T) {
	_, err := sets.SetDifference(nil, nil)
	if err == nil {
		t.Fatalf("Expected error when both sets are nil, got nil")
	}
}

// Test: set1 has elements, ALL elements in set2 (should become empty, thus return nil)
func TestSetDifference_allElementsRemoved(t *testing.T) {
	set1 := asSet(10, 20)
	set2 := asSet(10, 20, 30)
	result, err := sets.SetDifference(asSet(10, 20), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Test: set1 is empty, set2 is empty
func TestSetDifference_bothEmpty(t *testing.T) {
	set1 := asSet()
	set2 := asSet()
	result, err := sets.SetDifference(asSet(), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Test: set1 and set2 identical
func TestSetDifference_identicalSets(t *testing.T) {
	set1 := asSet(100, 200)
	set2 := asSet(100, 200)
	result, err := sets.SetDifference(asSet(100, 200), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}