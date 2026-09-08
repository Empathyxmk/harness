package public_tests

import (
	"ajpfuzzer"
	"testing"
)

func TestMainHandlesArgs(t *testing.T) {
	ajpfuzzer.FuzzerMain([]string{"test", "case"})
}