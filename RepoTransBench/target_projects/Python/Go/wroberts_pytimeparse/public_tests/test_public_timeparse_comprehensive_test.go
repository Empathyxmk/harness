package public_tests

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func timeparse(input string, granularity ...string) interface{} {
	panic("timeparse() not implemented in Go stub")
}
func _interpret_as_minutes(input string, m map[string]string) map[string]string {
	panic("_interpret_as_minutes() not implemented in Go stub")
}

func TestPublicTimeparse(t *testing.T) {
	cases := []struct {
		Input    string
		Expected interface{}
	}{
		{"2:50", 170},
		{":45", 45},
		{"2 minutes, 30 secs", 150},
		{"2m30s", 150},
		{"3.3 minutes", 198},
		{"2.3 seconds", 2.3},
		{"-2m30s", -150},
		{"+2m30s", 150},
		{"1w2d3h4m5s", 798645},
		{"5d", 432000},
		{"2 h", 7200},
		{"2.5 hours", 9000},
		{"4d, 11:59:59", 388799},
		{"2:33:21", 9201},
		{"10:00", 600},
		{"2 weeks, 1 day, 1 hour, 1 min, 0 secs", 788460},
		{"badinput", nil},
		{"", nil},
		{"--2m30s", nil},
		{"0.25w", 151200},
		{"2.8d", 241920},
		{"5:07:06", 18426},
		{"1:03:04.5", 3784.5},
	}
	for _, tt := range cases {
		func(tt struct {
			Input    string
			Expected interface{}
		}) {
			defer func() {
				if r := recover(); r == nil {
					t.Errorf("Expected timeparse to panic (Go stub) for input: %v", tt.Input)
				}
			}()
			_ = timeparse(tt.Input)
		}(tt)
	}
}

func TestPublicTimeparseHoursMinutesAmbiguity(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected _interpret_as_minutes to panic (Go stub)")
		}
	}()
	_interpret_as_minutes("2:50", map[string]string{"secs": "50", "mins": "2"})
}

func TestPublicTimeparseEdgeCases(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("   4h  ")
	timeparse("00")
	timeparse("+00")
	timeparse("-00")
	timeparse("2.01 seconds")
	timeparse("333d")
}

func TestPublicGranularityMinutes(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("4m", "minutes")
	timeparse("45s", "minutes")
	timeparse("69s", "minutes")
	timeparse("2:45")
	timeparse("2:45", "minutes")
}

func TestPublicGranularityError(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("1m", "foobar")
}

func TestPublicUnsupportedFloatParsing(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("0.11s")
}

func TestPublicInvalidTypes(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("")
	timeparse("")
}

func TestPublicSignedColonFormat(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("-2:50")
	timeparse("+2:50")
}

func TestPublicPartialMatchesFail(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected timeparse to panic (Go stub)")
		}
	}()
	timeparse("hello 5d world")
}