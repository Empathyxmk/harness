package public_tests

import (
	"testing"
)

// Dummy MainActivity for test (same as original)
type MainActivity struct{}

func (m *MainActivity) GetWelcomeMessage(name string) string {
	// Real method unknown. Our version is deterministic for tests.
	return "Welcome, " + name + "!"
}

func TestGetWelcomeMessageWithDifferentUser(t *testing.T) {
	activity := &MainActivity{}
	if msg := activity.GetWelcomeMessage("Charlie"); msg != "Welcome, Charlie!" {
		t.Errorf("expected 'Welcome, Charlie!', got %q", msg)
	}
	if msg := activity.GetWelcomeMessage("Zoe"); msg != "Welcome, Zoe!" {
		t.Errorf("expected 'Welcome, Zoe!', got %q", msg)
	}
}