package public_tests

import "testing"

// Simulated processInput for public cases: reverse string if not palindrome
func processInput(s string) string {
	n := len(s)
	isPalindrome := true
	for i := 0; i < n/2; i++ {
		if s[i] != s[n-1-i] {
			isPalindrome = false
			break
		}
	}
	if isPalindrome {
		return s
	}
	// reverse
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func TestProcessInputReverse(t *testing.T) {
	result := processInput("alpha")
	if result != "ahpla" {
		t.Errorf(`processInput("alpha") = %q, want %q`, result, "ahpla")
	}
}

func TestProcessInputPalindrome(t *testing.T) {
	result := processInput("noon")
	if result != "noon" {
		t.Errorf(`processInput("noon") = %q, want %q`, result, "noon")
	}
}