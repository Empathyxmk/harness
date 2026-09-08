package public_tests

import (
	"testing"
	"sets"
)

func asSet(vals ...int) sets.IntSet {
	return sets.NewIntSet(vals...)
}

// Public Test: Both sets are neither empty nor nil; basic set difference with no overlap
func TestSetDifference_noOverlap_nonNull_public(t *testing.T) {
	set1 := asSet(5)
	set2 := asSet(7)
	result, err := sets.SetDifference(asSet(5), set2)
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

// Public Test: set2 is empty - set1 unchanged
func TestSetDifference_set2Empty_public(t *testing.T) {
	set1 := asSet(9)
	set2 := asSet()
	result, err := sets.SetDifference(asSet(9), set2)
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

// Public Test: set1 has elements, some overlap with set2
func TestSetDifference_withOverlap_public(t *testing.T) {
	set1 := asSet(11, 13, 15)
	set2 := asSet(13, 17)
	expected := asSet(11, 15)
	result, err := sets.SetDifference(asSet(11, 13, 15), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if !result.Equal(expected) {
		t.Errorf("Expected %v, got %v", expected, result)
	}
}

// Public Test: set1 empty, set2 non-empty
func TestSetDifference_set1Empty_set2NonEmpty_public(t *testing.T) {
	result, err := sets.SetDifference(asSet(), asSet(21))
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Public Test: set1 is nil
func TestSetDifference_set1Nil_public(t *testing.T) {
	set2 := asSet(22)
	_, err := sets.SetDifference(nil, set2)
	if err == nil {
		t.Fatalf("Expected error for nil set1, got nil")
	}
}

// Public Test: set2 is nil
func TestSetDifference_set2Nil_public(t *testing.T) {
	set1 := asSet(42)
	_, err := sets.SetDifference(set1, nil)
	if err == nil {
		t.Fatalf("Expected error for nil set2, got nil")
	}
}

// Public Test: both sets are nil
func TestSetDifference_bothNil_public(t *testing.T) {
	_, err := sets.SetDifference(nil, nil)
	if err == nil {
		t.Fatalf("Expected error when both sets are nil, got nil")
	}
}

// Public Test: set1 has elements, ALL elements in set2 (should become empty, thus return nil)
func TestSetDifference_allElementsRemoved_public(t *testing.T) {
	set1 := asSet(101, 202)
	set2 := asSet(202, 101, 303)
	result, err := sets.SetDifference(asSet(101, 202), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Public Test: set1 is empty, set2 is empty
func TestSetDifference_bothEmpty_public(t *testing.T) {
	result, err := sets.SetDifference(asSet(), asSet())
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}

// Public Test: set1 and set2 identical
func TestSetDifference_identicalSets_public(t *testing.T) {
	set1 := asSet(333, 444)
	set2 := asSet(444, 333)
	result, err := sets.SetDifference(asSet(333, 444), set2)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if result != nil {
		t.Errorf("Expected nil, got %v", result)
	}
}