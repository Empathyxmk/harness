package original

import (
	"strconv"
	"testing"
)

type FizzBuzzRule struct {
	Divisor      int
	Substitution string
}

var rules = []FizzBuzzRule{
	{3 * 5, "FizzBuzz"},
	{3, "Fizz"},
	{5, "Buzz"},
}

func fizzbuzz(number int) string {
	for _, rule := range rules {
		if number%rule.Divisor == 0 {
			return rule.Substitution
		}
	}
	return strconv.Itoa(number)
}

func TestFizzbuzz(t *testing.T) {
	cases := []struct {
		Number int
		Word   string
	}{
		{1, "1"},
		{3, "Fizz"},
		{5, "Buzz"},
		{10, "Buzz"},
		{15, "FizzBuzz"},
		{16, "16"},
	}
	for _, tc := range cases {
		got := fizzbuzz(tc.Number)
		if got != tc.Word {
			t.Errorf("fizzbuzz(%d) expected %q, got %q", tc.Number, tc.Word, got)
		}
	}
}