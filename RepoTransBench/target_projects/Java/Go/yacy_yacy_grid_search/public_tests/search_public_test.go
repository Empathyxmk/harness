package public_tests

import (
	"testing"
	. "yacyyacygridsearch/tests"
)

func TestSearchPublic_QueryNormal(t *testing.T) {
	s := NewSearch()
	cases := []struct {
		in   string
		want string
	}{
		{"world", "Search results for: world"},
		{"123", "Search results for: 123"},
		{"test_case", "Search results for: test_case"},
	}
	for _, c := range cases {
		got, err := s.Query(c.in)
		if err != nil {
			t.Errorf("Unexpected error for input %q: %v", c.in, err)
		}
		if got != c.want {
			t.Errorf("Query(%q): want %q, got %q", c.in, c.want, got)
		}
	}
}

func TestSearchPublic_QueryEmptyVariants(t *testing.T) {
	s := NewSearch()
	tests := []string{"   ", "", "\t"}
	for _, q := range tests {
		got, err := s.Query(q)
		if err != nil {
			t.Errorf("Query(%q): unexpected error: %v", q, err)
		}
		want := "No query provided"
		if got != want {
			t.Errorf("Query(%q): want %q, got %q", q, want, got)
		}
	}
}

func TestSearchPublic_QueryErrorDifferentCase(t *testing.T) {
	s := NewSearch()
	errorStrs := []string{"ERROR", "Error"}
	for _, str := range errorStrs {
		_, err := s.Query(str)
		if err == nil {
			t.Errorf("Query(%q): expected error, got nil", str)
		} else if err.Error() != "Invalid query" {
			t.Errorf("Query(%q): expected error message 'Invalid query', got %q", str, err.Error())
		}
	}
}

func TestSearchPublic_IsServiceActiveStillTrue(t *testing.T) {
	s := NewSearch()
	if !s.IsServiceActive() {
		t.Error("IsServiceActive(): expected true")
	}
}