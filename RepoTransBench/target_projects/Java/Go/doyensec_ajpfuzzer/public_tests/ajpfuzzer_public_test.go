package public_tests

import (
	"ajpfuzzer"
	"testing"
)

func TestMainNoCrash(t *testing.T) {
	ajpfuzzer.FuzzerMain([]string{"--version"})
	ajpfuzzer.FuzzerMain([]string{})
}