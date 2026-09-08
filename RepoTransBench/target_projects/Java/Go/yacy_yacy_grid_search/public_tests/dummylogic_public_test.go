package public_tests

import (
	"testing"
	. "yacyyacygridsearch/tests"
)

func TestDummyLogicPublic_AddDifferentNumbers(t *testing.T) {
	d := NewDummyLogic()
	cases := []struct {
		a, b int
		want int
	}{
		{8, 7, 15},
		{-2, -3, -5},
		{15, -10, 5},
		{10, -10, 0},
		{-8, 8, 0},
		{10, 4, 14},
	}
	for _, c := range cases {
		got := d.Add(c.a, c.b)
		if got != c.want {
			t.Errorf("Add(%d, %d): want %d, got %d", c.a, c.b, c.want, got)
		}
	}
}

func TestDummyLogicPublic_IsPositiveDifferent(t *testing.T) {
	d := NewDummyLogic()
	if !d.IsPositive(1) {
		t.Error("IsPositive(1): expected true")
	}
	if d.IsPositive(-1) {
		t.Error("IsPositive(-1): expected false")
	}
	if d.IsPositive(0) {
		t.Error("IsPositive(0): expected false")
	}
}

func TestDummyLogicPublic_DescribeDifferentData(t *testing.T) {
	d := NewDummyLogic()
	cases := []struct {
		a, b int
		want string
	}{
		{-3, -3, "equal"},
		{12, 5, "greater"},
		{-10, 0, "less"},
	}
	for _, c := range cases {
		got := d.Describe(c.a, c.b)
		if got != c.want {
			t.Errorf("Describe(%d, %d): want %q, got %q", c.a, c.b, c.want, got)
		}
	}
}