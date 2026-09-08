package original

import (
	"math"
	"testing"

	"shekhargulati_30-seconds-of-java/tests"
	"shekhargulati_30-seconds-of-java/snippets"
)

func TestGcdOfArrayContaining1To5Is1(t *testing.T) {
	got := snippets.GCD([]int{1, 2, 3, 4, 5})
	if got != 1 {
		t.Errorf("expected gcd of [1 2 3 4 5] to be 1, got %d", got)
	}
}

func TestGcdOfTwoNumbers(t *testing.T) {
	got := snippets.GCD([]int{24, 18})
	if got != 6 {
		t.Errorf("expected gcd of [24 18] to be 6, got %d", got)
	}
}

func TestGcdOfSingleValueArray(t *testing.T) {
	got := snippets.GCD([]int{7})
	if got != 7 {
		t.Errorf("expected gcd of [7] to be 7, got %d", got)
	}
}

func TestGcdOfEmptyArrayIsZero(t *testing.T) {
	got := snippets.GCD([]int{})
	if got != 0 {
		t.Errorf("expected gcd of [] to be 0, got %d", got)
	}
}

func TestGcdOfArrayWithNegatives(t *testing.T) {
	got := snippets.GCD([]int{-24, 36})
	if got != 12 {
		t.Errorf("expected gcd of [-24, 36] to be 12, got %d", got)
	}
}

func TestLCMOfArrayContaining1To5Is60(t *testing.T) {
	got := snippets.LCM([]int{1, 2, 3, 4, 5})
	if got != 60 {
		t.Errorf("expected lcm of [1,2,3,4,5] to be 60, got %d", got)
	}
}

func TestLCMOfTwoNumbers(t *testing.T) {
	got := snippets.LCM([]int{12, 18})
	if got != 36 {
		t.Errorf("expected lcm of [12,18] to be 36, got %d", got)
	}
}

func TestLCMOfArrayWithZeroReturnsZero(t *testing.T) {
	got := snippets.LCM([]int{2, 0, 5})
	if got != 0 {
		t.Errorf("expected lcm of [2 0 5] to be 0, got %d", got)
	}
}

func TestLCMOfEmptyArrayIsZero(t *testing.T) {
	got := snippets.LCM([]int{})
	if got != 0 {
		t.Errorf("expected lcm of [] to be 0, got %d", got)
	}
}

func TestSumOfDigits(t *testing.T) {
	got := snippets.SumDigits(12345)
	if got != 15 {
		t.Errorf("expected sumDigits(12345) to be 15, got %d", got)
	}
}

func TestSumOfDigitsNegativeNumber(t *testing.T) {
	got := snippets.SumDigits(-12345)
	if got != 15 {
		t.Errorf("expected sumDigits(-12345) to be 15, got %d", got)
	}
}

func TestIsEven(t *testing.T) {
	valid := snippets.IsEven(6)
	if !valid {
		t.Error("expected isEven(6) to be true")
	}
	invalid := snippets.IsEven(7)
	if invalid {
		t.Error("expected isEven(7) to be false")
	}
}

func TestIsOdd(t *testing.T) {
	valid := snippets.IsOdd(3)
	if !valid {
		t.Error("expected isOdd(3) to be true")
	}
	invalid := snippets.IsOdd(44)
	if invalid {
		t.Error("expected isOdd(44) to be false")
	}
}

func TestIsPrime(t *testing.T) {
	if !snippets.IsPrime(7) {
		t.Error("expected 7 to be prime")
	}
	if snippets.IsPrime(8) {
		t.Error("expected 8 to not be prime")
	}
	// check for large non-prime
	if snippets.IsPrime(10000000) {
		t.Error("expected 10000000 to not be prime")
	}
}

func TestIsPalindromeNumber(t *testing.T) {
	if !snippets.IsPalindromeNumber(121) {
		t.Error("121 should be palindrome")
	}
	if snippets.IsPalindromeNumber(123) {
		t.Error("123 should not be palindrome")
	}
}

func TestFibonacciN(t *testing.T) {
	got := snippets.Fibonacci(10)
	if !slicesEqual(got, []int{0, 1, 1, 2, 3, 5, 8, 13, 21, 34}) {
		t.Errorf("expected fibonacci(10) to be [0 1 1 2 3 5 8 13 21 34], got %v", got)
	}
}

func TestReverseIntArray(t *testing.T) {
	got := snippets.Reverse([]int{1, 2, 3, 4, 5})
	if !slicesEqual(got, []int{5, 4, 3, 2, 1}) {
		t.Errorf("expected reverse([1 2 3 4 5]) to be [5 4 3 2 1], got %v", got)
	}
}

func TestReverseString(t *testing.T) {
	got := snippets.ReverseString("hello")
	if got != "olleh" {
		t.Errorf("expected reverseString('hello') to be 'olleh', got '%s'", got)
	}
}

func TestCountVowels(t *testing.T) {
	got := snippets.CountVowels("The quick brown fox")
	if got != 5 {
		t.Errorf("expected countVowels('The quick brown fox') to be 5, got %d", got)
	}
}

func TestFactorial(t *testing.T) {
	got := snippets.Factorial(5)
	if got != 120 {
		t.Errorf("expected factorial(5) to be 120, got %d", got)
	}
}

func TestFactorialZero(t *testing.T) {
	got := snippets.Factorial(0)
	if got != 1 {
		t.Errorf("expected factorial(0) to be 1, got %d", got)
	}
}

func TestIsPerfectSquare(t *testing.T) {
	if !snippets.IsPerfectSquare(16) {
		t.Error("expected 16 to be a perfect square")
	}
	if snippets.IsPerfectSquare(14) {
		t.Error("expected 14 to not be a perfect square")
	}
}

func TestSqrtInt(t *testing.T) {
	got := snippets.IntSqrt(17)
	if got != 4 {
		t.Errorf("expected intSqrt(17) to be 4, got %d", got)
	}
}

func TestRoundToNDecimalPlaces(t *testing.T) {
	got := snippets.RoundToNPlaces(3.1415926535, 2)
	if math.Abs(got-3.14) > 1e-9 {
		t.Errorf("expected roundToNPlaces(3.1415926535,2) ≈ 3.14, got %.10f", got)
	}
}

func TestArmstrongNumber(t *testing.T) {
	if !snippets.IsArmstrong(153) {
		t.Error("expected 153 as Armstrong number")
	}
	if snippets.IsArmstrong(123) {
		t.Error("expected 123 to not be Armstrong number")
	}
}

func TestFindMaxInIntArray(t *testing.T) {
	got := snippets.Max([]int{1, 3, 2, 0})
	if got != 3 {
		t.Errorf("expected max([1 3 2 0]) to be 3, got %d", got)
	}
}

func TestFindMinInIntArray(t *testing.T) {
	got := snippets.Min([]int{22, 3, 18, 99})
	if got != 3 {
		t.Errorf("expected min([22 3 18 99]) to be 3, got %d", got)
	}
}

func TestSecondLargestInArray(t *testing.T) {
	got := snippets.SecondLargest([]int{5, 1, 2, 5, 0, 4})
	if got != 4 {
		t.Errorf("expected secondLargest([5 1 2 5 0 4]) to be 4, got %d", got)
	}
}

func TestSecondSmallestInArray(t *testing.T) {
	got := snippets.SecondSmallest([]int{3, 1, 6, 5, 4, 2})
	if got != 2 {
		t.Errorf("expected secondSmallest([3 1 6 5 4 2]) to be 2, got %d", got)
	}
}

func TestFibonacciNth(t *testing.T) {
	got := snippets.FibonacciNth(7)
	if got != 13 {
		t.Errorf("expected fibonacciNth(7) to be 13, got %d", got)
	}
}

func TestReverseWordsInSentence(t *testing.T) {
	s := "This is a sentence"
	got := snippets.ReverseWords(s)
	expected := "sentence a is This"
	if got != expected {
		t.Errorf("expected reverseWords(%q) to be %q, got %q", s, expected, got)
	}
}

// Helper: compare two integer slices for equality
func slicesEqual(a, b []int) bool {
	if len(a) != len(b) {
		return false
	}
	for i, av := range a {
		if b[i] != av {
			return false
		}
	}
	return true
}