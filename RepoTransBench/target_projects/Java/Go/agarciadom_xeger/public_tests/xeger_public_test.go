package public_tests

import (
	"testing"
	"agarciadom_xeger/xeger"
)

func TestXegerPublic_LiteralGeneration(t *testing.T) {
	regex := "abcXYZ"
	gen := xeger.NewXeger(regex)
	result := gen.Generate()
	if result != "abcXYZ" {
		t.Fatalf("Expected 'abcXYZ', got %v", result)
	}
}

func TestXegerPublic_SimpleDigitGeneration(t *testing.T) {
	regex := "[4-6]{4}"
	gen := xeger.NewXeger(regex)
	result := gen.Generate()
	if len(result) != 4 {
		t.Errorf("Expected length 4, got %d", len(result))
	}
}

func TestXegerPublic_SimpleAlphaGeneration(t *testing.T) {
	regex := "[A-C]{3}"
	gen := xeger.NewXeger(regex)
	result := gen.Generate()
	if len(result) != 3 {
		t.Errorf("Expected length 3, got %d", len(result))
	}
}

func TestXegerPublic_RangeWithSpecialChar(t *testing.T) {
	regex := "[M-Q]{2}-[7-9]{2}"
	gen := xeger.NewXeger(regex)
	str := gen.Generate()
	if len(str) < 5 {
		t.Errorf("Expected at least 5 chars, got %d", len(str))
	}
	// TODO: regex match for stricter validity
}

func TestXegerPublic_RandomNumericGeneration(t *testing.T) {
	regex := "[98]{8}"
	gen := xeger.NewXeger(regex)
	str := gen.Generate()
	if len(str) != 8 {
		t.Errorf("Expected length 8, got %d", len(str))
	}
}