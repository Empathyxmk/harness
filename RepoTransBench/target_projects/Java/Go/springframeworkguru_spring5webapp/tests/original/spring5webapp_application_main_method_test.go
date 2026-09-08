package original

import (
	"testing"
	"spring5webapp"
)

func TestMainMethodRunsWithoutException(t *testing.T) {
	// The main method takes []string args, just call with empty args as in Java test.
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Calling main panicked: %v", r)
		}
	}()
	spring5webapp.Main([]string{})
}