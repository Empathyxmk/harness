package original

import (
	"testing"
)

// Simulated processInput reverses unless it's a palindrome.
func processInput(s string) string {
	// Check if palindrome
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
	// Reverse
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}

func TestProcessInputReverseExisting(t *testing.T) {
	result := processInput("test")
	if result != "tset" {
		t.Errorf("processInput(\"test\") = %q, want %q", result, "tset")
	}
}

func TestProcessInputPalindromeExisting(t *testing.T) {
	result := processInput("abba")
	if result != "abba" {
		t.Errorf("processInput(\"abba\") = %q, want %q", result, "abba")
	}
}