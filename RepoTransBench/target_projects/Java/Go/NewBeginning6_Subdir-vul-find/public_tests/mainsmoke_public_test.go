package public_tests

import (
	"testing"
	"newbeginning6subdir/org/example"
)

func TestMainLaunchPublic(t *testing.T) {
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("MainMain panicked: %v", r)
		}
	}()
	args := []string{"hello", "world", "--flag"}
	example.MainMain(args)
}