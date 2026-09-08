package public_tests

import (
	"testing"
	"spring5webapp"
)

func TestMainMethodRunsWithoutExceptionWithArgs(t *testing.T) {
	// As in Java, main is called with an argument.
	defer func() {
		if r := recover(); r != nil {
			t.Errorf("Calling main panicked: %v", r)
		}
	}()
	spring5webapp.Main([]string{"publicTestArg"})
}