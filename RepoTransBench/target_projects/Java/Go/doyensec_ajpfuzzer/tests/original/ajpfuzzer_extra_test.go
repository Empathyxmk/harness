package original

import (
	"ajpfuzzer"
	"testing"
)

func TestMainRunsAndDoesNotFail(t *testing.T) {
	// Just call main routine for coverage
	ajpfuzzer.FuzzerMain([]string{})
}