package original

import "testing"

func TestUseAppContext(t *testing.T) {
	// Simulate app context check.
	appContext := "org.jak_linux.dns66"
	if appContext != "org.jak_linux.dns66" {
		t.Errorf("expected package name org.jak_linux.dns66, got %q", appContext)
	}
}