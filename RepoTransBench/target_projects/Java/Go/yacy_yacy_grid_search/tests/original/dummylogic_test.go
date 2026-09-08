package original

import (
	"testing"
	. "yacyyacygridsearch/tests"
)

func TestDummyLogic_Add(t *testing.T) {
	d := NewDummyLogic()
	cases := []struct {
		a, b int
		want int
	}{
		{3, 4, 7},
		{-3, -4, -7},
		{-3, 3, 0},
		{0, 0, 0},
		{-3, 3, 0},
		{3, -3, 0},
	}
	for _, c := range cases {
		got := d.Add(c.a, c.b)
		if got != c.want {
			t.Errorf("Add(%d, %d): want %d, got %d", c.a, c.b, c.want, got)
		}
	}
}

func TestDummyLogic_IsPositive(t *testing.T) {
	d := NewDummyLogic()
	if !d.IsPositive(10) {
		t.Error("IsPositive(10): expected true")
	}
	if d.IsPositive(0) {
		t.Error("IsPositive(0): expected false")
	}
	if d.IsPositive(-4) {
		t.Error("IsPositive(-4): expected false")
	}
}

func TestDummyLogic_Describe(t *testing.T) {
	d := NewDummyLogic()
	cases := []struct {
		a, b int
		want string
	}{
		{5, 5, "equal"},
		{7, 2, "greater"},
		{3, 7, "less"},
	}
	for _, c := range cases {
		got := d.Describe(c.a, c.b)
		if got != c.want {
			t.Errorf("Describe(%d, %d): want %q, got %q", c.a, c.b, c.want, got)
		}
	}
}