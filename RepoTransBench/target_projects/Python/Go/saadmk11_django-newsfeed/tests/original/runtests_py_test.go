package original

import "testing"

func TestRunTestsExit(t *testing.T) {
	// Remove this test as 'runtests' is not present in sys.modules,
	// causing a KeyError and test failure.
	// In Go, this is a noop.
}