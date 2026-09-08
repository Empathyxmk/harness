package tests

import (
	"testing"
)

func TestEnumBasicBehavior(t *testing.T) {
	// Example enum (Gender) implementation
	type Gender int
	const (
		Male Gender = iota
		Female
	)

	// Testing equivalence
	assertEq(t, Male, 0)
	assertEq(t, Female, 1)

	// Testing string representation (simulate Python str(Enum))
	var strMale string
	switch Male {
	case 0:
		strMale = "Male"
	case 1:
		strMale = "Female"
	default:
		strMale = "Unknown"
	}
	assertEq(t, strMale, "Male")
}

func TestEnumComparisons(t *testing.T) {
	type Gender int
	const (
		Male Gender = iota
		Female
	)
	assertTrue(t, Male != Female)
	assertFalse(t, Male == Female)
}

func TestEnumMappingBehavior(t *testing.T) {
	type Gender int
	const (
		Male Gender = iota
		Female
	)
	names := map[Gender]string{
		Male:   "male",
		Female: "female",
	}
	assertEq(t, names[Male], "male")
	assertEq(t, names[Female], "female")
}

func TestEnumInvalidValuePanics(t *testing.T) {
	type Gender int
	defer func() {
		if r := recover(); r == nil {
			t.Fatalf("expected panic for invalid enum")
		}
	}()
	var g Gender = 2 // Invalid
	switch g {
	case 0, 1:
		// ok
	default:
		panic("invalid gender value")
	}
}