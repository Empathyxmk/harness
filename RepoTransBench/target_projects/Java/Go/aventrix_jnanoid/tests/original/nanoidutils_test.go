package original

import (
	"crypto/rand"
	"errors"
	"math"
	mathrand "math/rand"
	"reflect"
	"strings"
	"testing"
	"time"

	"aventrix_jnanoid/nanoid"
)

func TestDefaultRandomNanoId(t *testing.T) {
	nanoidStr := nanoid.RandomNanoId()
	if nanoidStr == "" {
		t.Errorf("Expected nanoid to be not empty")
	}
	if len(nanoidStr) != nanoid.DefaultSize {
		t.Errorf("Expected nanoid of length %d, got %d", nanoid.DefaultSize, len(nanoidStr))
	}
	for _, c := range nanoidStr {
		if !strings.ContainsRune(string(nanoid.DefaultAlphabet), c) {
			t.Errorf("Character %q not in default alphabet", c)
		}
	}
}

func TestRandomNanoIdWithCustomSize(t *testing.T) {
	length := 10
	nanoidStr, err := nanoid.RandomNanoIdCustom(rand.Reader, nanoid.DefaultAlphabet, length)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nanoidStr) != length {
		t.Errorf("Expected length %d, got %d", length, len(nanoidStr))
	}
}

func TestRandomNanoIdWithMinMaxSize(t *testing.T) {
	length := 1
	nanoidStr, err := nanoid.RandomNanoIdCustom(rand.Reader, nanoid.DefaultAlphabet, length)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nanoidStr) != length {
		t.Errorf("Expected nanoid of length %d, got %d", length, len(nanoidStr))
	}

	length = 1024
	nanoidStr, err = nanoid.RandomNanoIdCustom(rand.Reader, nanoid.DefaultAlphabet, length)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nanoidStr) != length {
		t.Errorf("Expected nanoid of length %d, got %d", length, len(nanoidStr))
	}
}

func TestRandomNanoIdZeroSize(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, nanoid.DefaultAlphabet, 0)
	if err == nil {
		t.Fatal("Expected error for size 0 but got nil")
	}
}

func TestRandomNanoIdNegativeSize(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, nanoid.DefaultAlphabet, -1)
	if err == nil {
		t.Fatal("Expected error for negative size but got nil")
	}
}

func TestRandomNanoIdNullRandom(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(nil, nanoid.DefaultAlphabet, 10)
	if err == nil {
		t.Fatal("Expected error for nil random source but got nil")
	}
}

func TestRandomNanoIdNullAlphabet(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, nil, 10)
	if err == nil {
		t.Fatal("Expected error for nil alphabet but got nil")
	}
}

func TestRandomNanoIdEmptyAlphabet(t *testing.T) {
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, []rune{}, 10)
	if err == nil {
		t.Fatal("Expected error for empty alphabet but got nil")
	}
}

func TestRandomNanoIdOversizedAlphabet(t *testing.T) {
	bigAlphabet := make([]rune, 256)
	for i := 0; i < 256; i++ {
		bigAlphabet[i] = rune('a' + (i % 26))
	}
	_, err := nanoid.RandomNanoIdCustom(rand.Reader, bigAlphabet, 10)
	if err == nil {
		t.Fatal("Expected error for oversized alphabet but got nil")
	}
}

func TestNanoIdIsUrlFriendly(t *testing.T) {
	nanoidStr := nanoid.RandomNanoId()
	if !nanoid.UrlFriendly.MatchString(nanoidStr) {
		t.Errorf("Nanoid is not URL friendly: %q", nanoidStr)
	}
}

func TestNanoIdUtilsPrivateConstructor(t *testing.T) {
	// Not applicable in Go: Private constructors for utility type; 
	// this is a coverage hack in Java, so in Go, nothing to test.
	// We'll at least check the package is importable and type present.
	if reflect.TypeOf(nanoid.DefaultAlphabet).Kind() != reflect.Slice {
		t.Errorf("DefaultAlphabet not a slice")
	}
}

func TestRandomNanoIdWithNonDefaultRandom(t *testing.T) {
	seed := int64(1234)
	rng := mathrand.New(mathrand.NewSource(seed))
	nanoidStr, err := nanoid.RandomNanoIdCustom(nanoid.NewPseudoReader(rng), nanoid.DefaultAlphabet, 11)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nanoidStr) != 11 {
		t.Errorf("Expected length 11, got %d", len(nanoidStr))
	}
}

func TestRandomNanoIdWithSmallAlphabet(t *testing.T) {
	alphabet := []rune{'a', 'b'}
	nanoidStr, err := nanoid.RandomNanoIdCustom(rand.Reader, alphabet, 6)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if len(nanoidStr) != 6 {
		t.Errorf("Expected length 6, got %d", len(nanoidStr))
	}
	for _, c := range nanoidStr {
		if c != 'a' && c != 'b' {
			t.Errorf("Expected 'a' or 'b', got %q", c)
		}
	}
}

func TestNanoIdUniqueness(t *testing.T) {
	nanoid1 := nanoid.RandomNanoId()
	nanoid2 := nanoid.RandomNanoId()
	if nanoid1 == nanoid2 {
		t.Errorf("Expected unique nanoids, but got equal ones: %q", nanoid1)
	}
}