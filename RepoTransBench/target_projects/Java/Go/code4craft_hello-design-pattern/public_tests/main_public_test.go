package public_tests

import (
	"testing"
)

func TestMainFuncPublic(t *testing.T) {
	// Simulate main("public")
	defer func() {
		if r := recover(); r != nil {
			t.Fatalf("main panicked: %v", r)
		}
	}()
	main()
}