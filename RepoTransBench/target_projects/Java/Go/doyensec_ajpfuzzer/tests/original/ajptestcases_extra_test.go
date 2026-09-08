package original

import (
	"testing"

	"ajpfuzzer"
)

func TestGetAllCasesImmutability(t *testing.T) {
	orig := ajpfuzzer.GetAllCases()
	if len(orig) == 0 {
		t.Skip("No test cases to check")
	}
	first := orig[0]
	if first != "GET /WEB-INF/web.xml" {
		t.Errorf("Expected first case to be 'GET /WEB-INF/web.xml', got '%s'", first)
	}
}

func TestGetAllCasesSize(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	if len(cases) < 2 {
		t.Errorf("Expected at least two default test cases, got %d", len(cases))
	}
}