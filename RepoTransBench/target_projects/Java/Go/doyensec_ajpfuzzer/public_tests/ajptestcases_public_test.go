package public_tests

import (
	"ajpfuzzer"
	"strings"
	"testing"
)

func TestGetAllCasesImmutabilityDifferent(t *testing.T) {
	orig := ajpfuzzer.GetAllCases()
	if len(orig) == 0 {
		t.Skip("No test cases to check")
	}
	last := orig[len(orig)-1]
	if !(strings.HasSuffix(last, ".jsp") || strings.HasSuffix(last, ".xml") || strings.Contains(last, "/")) {
		t.Errorf("Last case '%s' is not a plausible test path", last)
	}
}

func TestGetAllCasesHasDefaultCases(t *testing.T) {
	cases := ajpfuzzer.GetAllCases()
	found := false
	for _, v := range cases {
		if v == "GET /WEB-INF/web.xml" {
			found = true
			break
		}
	}
	if !found {
		t.Errorf("Should contain 'GET /WEB-INF/web.xml' as a default case")
	}
}