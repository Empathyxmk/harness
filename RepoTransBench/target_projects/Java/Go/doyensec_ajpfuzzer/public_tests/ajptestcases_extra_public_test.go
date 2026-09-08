package public_tests

import (
	"ajpfuzzer"
	"strings"
	"testing"
)

func TestGetAllCasesNonEmpty(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	if len(cases) == 0 {
		t.Error("Should not be empty")
	}
}

func TestGetAllCasesContainsTest(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	found := false
	for _, s := range cases {
		if strings.HasPrefix(s, "GET ") {
			found = true
			break
		}
	}
	if !found {
		t.Error("At least one case should start with 'GET '")
	}
}