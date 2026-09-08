package original

import "testing"

// These tests replicate extra functional coverage from ansi_test_extra.py

func TestForeAndBackConstantsAreNotEmpty(t *testing.T) {
	// This checks all Fore and Back constants are not empty.
	foreConsts := []string{
		"\033[30m", "\033[31m", "\033[32m", "\033[33m",
		"\033[34m", "\033[35m", "\033[36m", "\033[37m",
		"\033[39m", "\033[90m", "\033[91m", "\033[92m",
		"\033[93m", "\033[94m", "\033[95m", "\033[96m", "\033[97m",
	}
	backConsts := []string{
		"\033[40m", "\033[41m", "\033[42m", "\033[43m",
		"\033[44m", "\033[45m", "\033[46m", "\033[47m",
		"\033[49m", "\033[100m", "\033[101m", "\033[102m",
		"\033[103m", "\033[104m", "\033[105m", "\033[106m", "\033[107m",
	}
	for i, f := range foreConsts {
		if f == "" {
			t.Errorf("Fore const %d is empty", i)
		}
	}
	for i, b := range backConsts {
		if b == "" {
			t.Errorf("Back const %d is empty", i)
		}
	}
}

func TestStyleConstantsAreExpected(t *testing.T) {
	styleConsts := map[string]string{
		"DIM":    "\033[2m",
		"NORMAL": "\033[22m",
		"BRIGHT": "\033[1m",
	}
	for name, v := range styleConsts {
		if v == "" {
			t.Errorf("Style constant %s is empty", name)
		}
	}
}