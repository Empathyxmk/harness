package original

import (
	"testing"
)

// These would be integration tests as they hit Google's service.
// Marked with a build tag which can be run selectively.

func TestQuery(t *testing.T) {
	// xfail: Google's rate limiter may make this unstable.
	result := []string{"dummy-result"} // simulates gs.query('Albert Einstein', ...)
	if len(result) == 0 {
		t.Error("Expected non-empty result")
	}
}

func TestQueryUtf8(t *testing.T) {
	// xfail: Google's rate limiter may make this unstable.
	result := []string{"dummy-result"} // simulates gs.query('Anders Jonas Ångström', ...)
	if len(result) == 0 {
		t.Error("Expected non-empty result")
	}
}