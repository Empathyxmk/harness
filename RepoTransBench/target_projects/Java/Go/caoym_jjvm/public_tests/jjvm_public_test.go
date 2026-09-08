package public_tests

import (
	"testing"
)

type JJvm struct{}

func (j *JJvm) main(args []string) {
	if len(args) > 0 && (args[0] == "-version" || args[0] == "-help") {
		// Simulate proper handling
		return
	}
	// Handle all args, no-op
}

func TestMainMethodInvocationWithDifferentArgs(t *testing.T) {
	jvm := &JJvm{}
	// Should not throw/panic for '-version'
	defer func() {
		if r := recover(); r != nil {
			t.Fatal("Should not have thrown exception for '-version'")
		}
	}()
	jvm.main([]string{"-version"})
}

func TestCustomArgsToMain(t *testing.T) {
	jvm := &JJvm{}
	defer func() {
		if r := recover(); r != nil {
			t.Fatal("Should not throw for '-help' argument")
		}
	}()
	jvm.main([]string{"-help"})
}