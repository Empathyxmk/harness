package original

import (
	"testing"
	. "yacyyacygridsearch/tests"
)

func TestSearch_QueryNormal(t *testing.T) {
	s := NewSearch()
	got, err := s.Query("hello")
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	want := "Search results for: hello"
	if got != want {
		t.Errorf("Expected %q, got %q", want, got)
	}
}

func TestSearch_QueryEmpty(t *testing.T) {
	s := NewSearch()
	tests := []string{"", "  ", "", "\t", "   "}
	for _, q := range tests {
		got, err := s.Query(q)
		if err != nil {
			t.Errorf("For query %q, did not expect error: %v", q, err)
		}
		want := "No query provided"
		if got != want {
			t.Errorf("For query %q: expected %q, got %q", q, want, got)
		}
	}
}

func TestSearch_QueryError(t *testing.T) {
	s := NewSearch()
	_, err := s.Query("error")
	if err == nil {
		t.Fatal("Expected error for query 'error', got nil")
	}
	if err.Error() != "Invalid query" {
		t.Errorf("Expected error message 'Invalid query', got %q", err.Error())
	}
}

func TestSearch_IsServiceActive(t *testing.T) {
	s := NewSearch()
	if !s.IsServiceActive() {
		t.Error("Expected service to be active")
	}
}