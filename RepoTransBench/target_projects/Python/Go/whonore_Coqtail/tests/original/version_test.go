package original

import (
	"strconv"
	"strings"
	"testing"
)

func parseVersion(v string) (int, int, int) {
	// Copying logic from public test
	fields := strings.SplitN(v, ".", 3)
	a, b, c := 0, 0, 0
	if len(fields) > 0 {
		a, _ = strconv.Atoi(fields[0])
	}
	if len(fields) > 1 {
		s := ""
		for i := 0; i < len(fields[1]); i++ {
			if '0' <= fields[1][i] && fields[1][i] <= '9' {
				s += string(fields[1][i])
			} else {
				break
			}
		}
		b, _ = strconv.Atoi(s)
	}
	if len(fields) > 2 {
		s := ""
		for i := 0; i < len(fields[2]); i++ {
			if '0' <= fields[2][i] && fields[2][i] <= '9' {
				s += string(fields[2][i])
			} else {
				break
			}
		}
		c, _ = strconv.Atoi(s)
	}
	return a, b, c
}

func TestMatcher(t *testing.T) {
	tests := []struct {
		input    string
		expected [3]int
	}{
		{"1.2.3", [3]int{1, 2, 3}},
		{"1.2pl3", [3]int{1, 2, 3}},
		{"1.2", [3]int{1, 2, 0}},
		{"1.2+alpha3", [3]int{1, 2, 0}},
		{"1.2+alpha", [3]int{1, 2, 0}},
	}
	for _, tc := range tests {
		a, b, c := parseVersion(tc.input)
		expA, expB, expC := tc.expected[0], tc.expected[1], tc.expected[2]
		if a != expA || b != expB || c != expC {
			t.Errorf("parseVersion(%q) = (%d,%d,%d), want (%d,%d,%d)", tc.input, a, b, c, expA, expB, expC)
		}
	}
}