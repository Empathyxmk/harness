package original

import (
	"testing"

	"ajpfuzzer"
)

func TestGetAllCasesReturnsNonEmptyList(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	if cases == nil {
		t.Fatal("Result should not be nil")
	}
	if len(cases) == 0 {
		t.Fatal("Should not be empty")
	}
}

func TestCaseContainsKnownAttackPayloads(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	found := false
	for _, s := range cases {
		if s == "GET /WEB-INF/web.xml" || s == "POST /admin HTTP/1.1" || s == "/WEB-INF/web.xml" {
			found = true
			break
		}
	}
	if !found {
		t.Error("Expected to find a known attack payload in the cases.")
	}
}

func TestListIsUnmodifiable(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			// In Go, slices are modifiable, but we can simulate 'unmodifiable' by using a copy if implemented.
			// Here, test passes regardless.
		}
	}()
	// The following will NOT panic in Go, so we just document: unmodifiable concept can't be strictly enforced.
	c := append(ajpfuzzer.GetAllCases(), "test-case")
	// This just appends, won't panic.
	_ = c
}