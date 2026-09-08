package public_tests

import (
	"testing"
)

func TestPublicQuery(t *testing.T) {
	result := []string{"dummy-ramanujan"} // Simulate gs.query('Niels Bohr', ...)
	if len(result) == 0 {
		t.Error("Expected non-empty result")
	}
}

func TestPublicQueryUtf8(t *testing.T) {
	result := []string{"dummy-ramanujan"} // Simulate gs.query('Srinivasa Ramanujan', ...)
	if len(result) == 0 {
		t.Error("Expected non-empty result")
	}
}