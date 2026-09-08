package public_tests

import (
	"testing"
)

func dataPublic() []int {
	return []int{11, 12, 13, 14}
}

func TestSumDataPublic(t *testing.T) {
	data := dataPublic()
	want := 50
	got := 0
	for _, v := range data {
		got += v
	}
	if got != want {
		t.Errorf("expected sum 50, got %d", got)
	}
}

func TestSquarePublic(t *testing.T) {
	var tests = []struct {
		x        int
		expected int
	}{
		{2, 4},
		{5, 25},
		{10, 100},
	}
	for _, tc := range tests {
		got := tc.x * tc.x
		if got != tc.expected {
			t.Errorf("for %d, expected %d, got %d", tc.x, tc.expected, got)
		}
	}
}