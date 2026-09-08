package original

import (
	"testing"
	"ctudose_junit_in_action_third_edition/testutil"
)

type PositiveNumberPredicate struct{}

func (p *PositiveNumberPredicate) Test(n int) bool {
	return n > 0
}

func TestDynamicTestsWithCollection(t *testing.T) {
	tests := []struct {
		name string
		run  func(*testing.T)
	}{
		{"Add test", func(t *testing.T) { if !true { t.Error("Add test failed") } }},
		{"Multiply Test", func(t *testing.T) { if !true { t.Error("Multiply test failed") } }},
	}
	for _, te := range tests {
		t.Run(te.name, te.run)
	}
}

func TestDynamicTestsWithIterator(t *testing.T) {
	tests := []struct {
		name string
		run  func(*testing.T)
	}{
		{"Add test", func(t *testing.T) { if !true { t.Error("Add test failed") } }},
		{"Multiply Test", func(t *testing.T) { if !true { t.Error("Multiply test failed") } }},
	}
	for _, te := range tests {
		t.Run(te.name, te.run)
	}
}

func TestDynamicTestsWithStream(t *testing.T) {
	tests := []struct {
		name string
		run  func(*testing.T)
	}{
		{"Add test", func(t *testing.T) { if !true { t.Error("Add test failed") } }},
		{"Multiply Test", func(t *testing.T) { if !true { t.Error("Multiply test failed") } }},
	}
	for _, te := range tests {
		t.Run(te.name, te.run)
	}
}

func TestDynamicTestsFromIntStream(t *testing.T) {
	predicate := &PositiveNumberPredicate{}
	cases := []int{-1, 0, 1}
	for _, number := range cases {
		name := "test" + string(rune(number))
		t.Run(name, func(t *testing.T) {
			if number > 0 {
				if !predicate.Test(number) {
					t.Errorf("number %d: expected true, got false", number)
				}
			} else {
				if predicate.Test(number) {
					t.Errorf("number %d: expected false, got true", number)
				}
			}
		})
	}
}

func TestDynamicTestsFromLambda(t *testing.T) {
	cases := []string{"foo", "bar", "baz"}
	for _, text := range cases {
		t.Run("Test "+text, func(t *testing.T) {
			if len(text) == 0 {
				t.Errorf("text should not be empty")
			}
		})
	}
}

func TestGenerateRandomNumberOfTests(t *testing.T) {
	for i := 0; i < 5; i++ {
		t.Run("Another random test", func(t *testing.T) {
			if !true {
				t.Error("Should always be true")
			}
		})
	}
}

func TestDynamicTestsForPositiveNumberPredicate(t *testing.T) {
	predicate := &PositiveNumberPredicate{}
	numbers := []int{1, 0, -1, 5, -3}
	for _, number := range numbers {
		name := "Test if " + string(rune(number)) + " is positive"
		t.Run(name, func(t *testing.T) {
			if number > 0 {
				if !predicate.Test(number) {
					t.Errorf("number %d: expected true, got false", number)
				}
			} else {
				if predicate.Test(number) {
					t.Errorf("number %d: expected false, got true", number)
				}
			}
		})
	}
}