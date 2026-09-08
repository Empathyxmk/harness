package original

import (
	"testing"
)

func TestConstantsPyVersionAndDefaults(t *testing.T) {
	const VERSION = "0.4.3"
	const DEFAULT_DELAY = 0.2
	const LOOP_DELAY = 0.1

	if VERSION != "0.4.3" {
		t.Errorf("VERSION was %s, want 0.4.3", VERSION)
	}
	if DEFAULT_DELAY != 0.2 {
		t.Errorf("Got DEFAULT_DELAY=%v", DEFAULT_DELAY)
	}
	if LOOP_DELAY != 0.1 {
		t.Errorf("Got LOOP_DELAY=%v", LOOP_DELAY)
	}
}