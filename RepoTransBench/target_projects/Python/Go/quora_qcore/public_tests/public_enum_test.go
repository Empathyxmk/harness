package public_tests

import (
	"testing"
)

func TestGenderEnumValues(t *testing.T) {
	type Gender int
	const (
		Male Gender = iota
		Female
	)
	if Male != 0 {
		t.Fatalf("expected Male == 0, got %v", Male)
	}
	if Female != 1 {
		t.Fatalf("expected Female == 1, got %v", Female)
	}
}

func TestGenderEnumStringConversion(t *testing.T) {
	type Gender int
	const (
		Male Gender = iota
		Female
	)
	getName := func(g Gender) string {
		switch g {
		case Male:
			return "male"
		case Female:
			return "female"
		default:
			return "unknown"
		}
	}
	if getName(Male) != "male" {
		t.Fatalf("expected getName(Male) == 'male'")
	}
	if getName(Female) != "female" {
		t.Fatalf("expected getName(Female) == 'female'")
	}
	if getName(100) != "unknown" {
		t.Fatalf("expected getName(100) == 'unknown'")
	}
}