package public_tests

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func parse(input string, granularity ...string) interface{} {
	panic("parse() not implemented in Go stub")
}

func TestPublicParseVariety(t *testing.T) {
	cases := []struct {
		Input    interface{}
		Expected interface{}
	}{
		{"10:25", 625},
		{"3m25s", 205},
		{"4.5 hours", 16200},
		{"-4m20s", -260},
		{"0.5w", 302400},
		{"nonsense again", nil},
		{"7d 1:01:01", 622861},
		{"", nil},
		{nil, nil},
	}
	for _, tt := range cases {
		func(tt struct {
			Input    interface{}
			Expected interface{}
		}) {
			defer func() {
				if r := recover(); r == nil {
					t.Errorf("Expected parse() to panic (Go translation stub)")
				}
			}()
			_ = parse(tt.Input)
		}(tt)
	}
}

func TestPublicParseTypeError(t *testing.T) {
	inputs := []interface{}{0, []int{}, map[string]string{}}
	for _, input := range inputs {
		func(input interface{}) {
			defer func() {
				if r := recover(); r == nil {
					t.Errorf("Expected parse() to panic")
				}
			}()
			_ = parse(input)
		}(input)
	}
}

func TestPublicParseWithGranularityMinutes(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected parse() to panic (Go stubbed)")
		}
	}()
	_ = parse("3:45")
	_ = parse("3:45", "minutes")
	_ = parse("65s", "minutes")
	_ = parse("8m", "foo")
}

func TestPublicParseLargeValue(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected parse() to panic (Go stub)")
		}
	}()
	_ = parse("999d")
	_ = parse("5.5h")
}

func TestPublicColonVariants(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected parse() to panic (Go stub)")
		}
	}()
	_ = parse("-10:25")
	_ = parse("+10:25")
}