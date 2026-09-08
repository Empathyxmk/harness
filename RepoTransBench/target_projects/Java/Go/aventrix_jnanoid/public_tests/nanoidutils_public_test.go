package public_tests

import (
	"crypto/rand"
	"testing"
	"strings"
	"aventrix_jnanoid/nanoid"
)

func charArrayToString(arr []rune) string {
	return string(arr)
}

func TestRandomNanoIdNoArgsLengthAndAlphabet(t *testing.T) {
	nanoidStr := nanoid.RandomNanoId()
	if nanoidStr == "" {
		t.Errorf("Expected nanoid to be not empty")
	}
	if len(nanoidStr) != 21 {
		t.Errorf("Expected nanoid of length 21, got %d", len(nanoidStr))
	}
	defaultAlphabetStr := charArrayToString(nanoid.DefaultAlphabet)
	for _, c := range nanoidStr {
		if !strings.ContainsRune(defaultAlphabetStr, c) {
			t.Errorf("Character %q not in default alphabet", c)
		}
	}
}

func TestRandomNanoIdCustomAlphabetPublic(t *testing.T) {
	customAlphabet := []rune{'a', 'B', '4', '!'}
	size := 13
	nanoidStr, err := nanoid.RandomNanoIdCustom(rand.Reader, customAlphabet, size)
	if err != nil {
		t.Fatalf("Error in nanoid: %v", err)
	}
	if nanoidStr == "" {
		t.Errorf("Expected nanoid to be not empty")
	}
	if len(nanoidStr) != size {
		t.Errorf("Expected nanoid of length %d, got %d", size, len(nanoidStr))
	}
	alphabetStr := charArrayToString(customAlphabet)
	for _, c := range nanoidStr {
		if !strings.ContainsRune(alphabetStr, c) {
			t.Errorf("Character %q not in custom alphabet", c)
		}
	}
}

func TestRandomNanoIdNullAlphabetPublic(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, nil, 10)
	if err == nil {
		t.Fatalf("Expected error for nil alphabet but got nil")
	}
}

func TestRandomNanoIdEmptyAlphabetPublic(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, []rune{}, 8)
	if err == nil {
		t.Fatalf("Expected error for empty alphabet but got nil")
	}
}

func TestRandomNanoIdTooShortLengthPublic(t *testing.T) {
	alphabet := []rune{'a', 'b'}
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, alphabet, 0)
	if err == nil {
		t.Fatalf("Expected error for length 0 but got nil")
	}
}

func TestRandomNanoIdNegativeLengthPublic(t *testing.T) {
	alphabet := []rune{'a', 'b', 'c'}
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, alphabet, -5)
	if err == nil {
		t.Fatalf("Expected error for negative length but got nil")
	}
}

func TestRandomNanoIdAlphabetTooLongPublic(t *testing.T) {
	alphabet := make([]rune, 300)
	for i := 0; i < 300; i++ {
		alphabet[i] = rune(32 + (i % 94)) // printable ASCII
	}
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, alphabet, 8)
	if err == nil {
		t.Fatalf("Expected error for alphabet length > 255 but got nil")
	}
}

func TestRandomNanoIdCustomRandomPublic(t *testing.T) {
	rng := nanoid.NewPseudoReaderWithSeed(42)
	alphabet := []rune{'Q', 'W', 'E'}
	size := 6
	nanoidStr1, err := nanoid.RandomNanoIdCustom(rng, alphabet, size)
	if err != nil {
		t.Fatalf("Error in nanoid: %v", err)
	}
	if len(nanoidStr1) != size {
		t.Errorf("Expected nanoid of length %d, got %d", size, len(nanoidStr1))
	}
	alphabetStr := charArrayToString(alphabet)
	for _, c := range nanoidStr1 {
		if !strings.ContainsRune(alphabetStr, c) {
			t.Errorf("Character %q not in custom alphabet", c)
		}
	}
	// Deterministic expectation
	rng2 := nanoid.NewPseudoReaderWithSeed(42)
	expected, _ := nanoid.RandomNanoIdCustom(rng2, alphabet, size)
	if nanoidStr1 != expected {
		t.Errorf("Expected deterministic nanoid, got %q, expected %q", nanoidStr1, expected)
	}
}

func TestRandomNanoIdDefaultRandomPublic(t *testing.T) {
	length := 17
	alphabet := nanoid.DefaultAlphabet
	nanoidStr, err := nanoid.RandomNanoIdCustom(rand.Reader, alphabet, length)
	if err != nil {
		t.Fatalf("Error in nanoid: %v", err)
	}
	if len(nanoidStr) != length {
		t.Errorf("Expected nanoid of length %d, got %d", length, len(nanoidStr))
	}
	defaultAlphabetStr := charArrayToString(alphabet)
	for _, c := range nanoidStr {
		if !strings.ContainsRune(defaultAlphabetStr, c) {
			t.Errorf("Character %q not in default alphabet", c)
		}
	}
}