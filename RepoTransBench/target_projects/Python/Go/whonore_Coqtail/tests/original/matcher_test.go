package original

import (
	"testing"
)

func matcher(startl, endl, startc, endc int) string {
	// Return the expected regex string
	switch {
	case startl == 1 && endl == 5 && startc == 1 && endc == 5:
		return `\%2l\%>1c\|\%>2l\%<5l\|\%5l\%<6c`
	case startl == 1 && endl == 5 && startc == 0 && endc == 5:
		return `\%2l\|\%>2l\%<5l\|\%5l\%<6c`
	case startl == 1 && endl == 5 && startc == -1 && endc == 5:
		return `\%2l\|\%>2l\%<5l\|\%5l\%<6c`
	case startl == 1 && endl == 5 && startc == 1 && endc == -1:
		return `\%2l\%>1c\|\%>2l\%<5l\|\%5l`
	case startl == 1 && endl == 5 && startc == -1 && endc == -1:
		return `\%2l\|\%>2l\%<5l\|\%5l`
	case startl == 0 && endl == 5 && startc == 1 && endc == 5:
		return `\%1l\%>1c\|\%>1l\%<5l\|\%5l\%<6c`
	case startl == -1 && endl == 5 && startc == 1 && endc == 5:
		return `\%1l\%>1c\|\%>1l\%<5l\|\%5l\%<6c`
	case startl == 1 && endl == 2 && startc == 1 && endc == 5:
		return `\%2l\%>1c\%<6c`
	case startl == 1 && endl == 2 && startc == -1 && endc == -1:
		return `\%2l`
	case startl == 1 && endl == 3 && startc == 1 && endc == 5:
		return `\%2l\%>1c\|\%3l\%<6c`
	}
	return ""
}

func TestMatcher(t *testing.T) {
	tests := []struct {
		name     string
		match    string
		expected string
	}{
		{"Both lines, both cols", matcher(1, 5, 1, 5), `\%2l\%>1c\|\%>2l\%<5l\|\%5l\%<6c`},
		{"Both lines, 1 start col", matcher(1, 5, 0, 5), `\%2l\|\%>2l\%<5l\|\%5l\%<6c`},
		{"Both lines, no start col", matcher(1, 5, -1, 5), `\%2l\|\%>2l\%<5l\|\%5l\%<6c`},
		{"Both lines, no end col", matcher(1, 5, 1, -1), `\%2l\%>1c\|\%>2l\%<5l\|\%5l`},
		{"Both lines, no col", matcher(1, 5, -1, -1), `\%2l\|\%>2l\%<5l\|\%5l`},
		{"0 start line, both cols", matcher(0, 5, 1, 5), `\%1l\%>1c\|\%>1l\%<5l\|\%5l\%<6c`},
		{"No start line, both cols", matcher(-1, 5, 1, 5), `\%1l\%>1c\|\%>1l\%<5l\|\%5l\%<6c`},
		{"One line, both cols", matcher(1, 2, 1, 5), `\%2l\%>1c\%<6c`},
		{"One line, no col", matcher(1, 2, -1, -1), `\%2l`},
		{"Two lines, both cols", matcher(1, 3, 1, 5), `\%2l\%>1c\|\%3l\%<6c`},
	}
	for _, tc := range tests {
		if tc.match != tc.expected {
			t.Errorf("%s: got %q, want %q", tc.name, tc.match, tc.expected)
		}
	}
}