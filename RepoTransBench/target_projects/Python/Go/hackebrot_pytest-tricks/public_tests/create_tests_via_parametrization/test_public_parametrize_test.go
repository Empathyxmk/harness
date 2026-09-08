package public_tests

import (
	"strconv"
	"testing"
)

var publicRules = []struct {
	Divisor      int
	Substitution string
}{
	{2 * 7, "FooBar"},
	{2, "Foo"},
	{7, "Bar"},
}

func foobar(number int) string {
	for _, rule := range publicRules {
		if number%rule.Divisor == 0 {
			return rule.Substitution
		}
	}
	return strconv.Itoa(number)
}

func TestFoobar(t *testing.T) {
	cases := []struct {
		Number int
		Word   string
	}{
		{1, "1"},
		{2, "Foo"},
		{7, "Bar"},
		{14, "FooBar"},
		{8, "Foo"},
		{13, "13"},
	}
	for _, tc := range cases {
		got := foobar(tc.Number)
		if got != tc.Word {
			t.Errorf("foobar(%d) expected %s, got %s", tc.Number, tc.Word, got)
		}
	}
}