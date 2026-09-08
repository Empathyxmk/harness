package original

import (
	"testing"
)

// NOTE: These tests are symbolic/structural as the actual ANSI const definitions and methods
//       would need to be implemented in Go. This test suite should match logic and assertions from Python.

func TestForeAttributes(t *testing.T) {
	assertEqual(t, Fore.BLACK, "\033[30m")
	assertEqual(t, Fore.RED, "\033[31m")
	assertEqual(t, Fore.GREEN, "\033[32m")
	assertEqual(t, Fore.YELLOW, "\033[33m")
	assertEqual(t, Fore.BLUE, "\033[34m")
	assertEqual(t, Fore.MAGENTA, "\033[35m")
	assertEqual(t, Fore.CYAN, "\033[36m")
	assertEqual(t, Fore.WHITE, "\033[37m")
	assertEqual(t, Fore.RESET, "\033[39m")
	assertEqual(t, Fore.LIGHTBLACK_EX, "\033[90m")
	assertEqual(t, Fore.LIGHTRED_EX, "\033[91m")
	assertEqual(t, Fore.LIGHTGREEN_EX, "\033[92m")
	assertEqual(t, Fore.LIGHTYELLOW_EX, "\033[93m")
	assertEqual(t, Fore.LIGHTBLUE_EX, "\033[94m")
	assertEqual(t, Fore.LIGHTMAGENTA_EX, "\033[95m")
	assertEqual(t, Fore.LIGHTCYAN_EX, "\033[96m")
	assertEqual(t, Fore.LIGHTWHITE_EX, "\033[97m")
}

func TestBackAttributes(t *testing.T) {
	assertEqual(t, Back.BLACK, "\033[40m")
	assertEqual(t, Back.RED, "\033[41m")
	assertEqual(t, Back.GREEN, "\033[42m")
	assertEqual(t, Back.YELLOW, "\033[43m")
	assertEqual(t, Back.BLUE, "\033[44m")
	assertEqual(t, Back.MAGENTA, "\033[45m")
	assertEqual(t, Back.CYAN, "\033[46m")
	assertEqual(t, Back.WHITE, "\033[47m")
	assertEqual(t, Back.RESET, "\033[49m")
	assertEqual(t, Back.LIGHTBLACK_EX, "\033[100m")
	assertEqual(t, Back.LIGHTRED_EX, "\033[101m")
	assertEqual(t, Back.LIGHTGREEN_EX, "\033[102m")
	assertEqual(t, Back.LIGHTYELLOW_EX, "\033[103m")
	assertEqual(t, Back.LIGHTBLUE_EX, "\033[104m")
	assertEqual(t, Back.LIGHTMAGENTA_EX, "\033[105m")
	assertEqual(t, Back.LIGHTCYAN_EX, "\033[106m")
	assertEqual(t, Back.LIGHTWHITE_EX, "\033[107m")
}

func TestStyleAttributes(t *testing.T) {
	assertEqual(t, Style.DIM, "\033[2m")
	assertEqual(t, Style.NORMAL, "\033[22m")
	assertEqual(t, Style.BRIGHT, "\033[1m")
}

// Helper for assertion
func assertEqual(t *testing.T, a interface{}, b interface{}) {
	if a != b {
		t.Fatalf("expected %v == %v", a, b)
	}
}