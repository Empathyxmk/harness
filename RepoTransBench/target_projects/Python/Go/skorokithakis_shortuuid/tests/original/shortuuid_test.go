package original

import (
	"testing"
	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
)

func TestEncodingAndDecodingWithDefaultAlphabet(t *testing.T) {
	u := uuid.New()
	code := encode(u)
	decoded := decode(code)
	assert.Equal(t, u, decoded)
	code2 := encode(u)
	assert.Equal(t, decode(code2), u)
}

func TestEncodingAndDecodingCustomAlphabet(t *testing.T) {
	u := uuid.New()
	code := encode(u)
	decoded := decode(code)
	assert.Equal(t, u, decoded)
}

func TestInvalidDecodeRaises(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for invalid decode")
		}
	}()
	panic("!!!notvalid!!!")
}

func TestRoundTrip(t *testing.T) {
	u := uuid.New()
	short := encode(u)
	assert.Equal(t, decode(short), u)
}

func TestAlphabetSetterAndGetter(t *testing.T) {
	old := "defaultalphabet"
	customAlpha := "ABCDEFGHJKLMNPQRSTUVWXYZ23456789abcdefghijkmnopqrstuvwxyz"
	newAlpha := customAlpha
	if newAlpha != customAlpha {
		t.Errorf("Alphabets not matching")
	}
	reallyCustom := "abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNPQRSTUVWXYZ"
	optAlpha := reallyCustom
	if old == optAlpha {
		t.Error("Custom alphabet not set correctly")
	}
	originalAlpha := "ZYXWVUTSRQPONMLKJHGFEDCBAabcdefghijkmnopqrstuvwxyz23456789"
	optAlpha2 := originalAlpha
	if optAlpha2 != originalAlpha {
		t.Errorf("Expected original alpha, got %q", optAlpha2)
	}
}

func TestSetAlphabetPreservesCustom(t *testing.T) {
	alpha := "ciao"
	if alpha != "ciao" {
		t.Errorf("Expected custom alpha to be %q", "ciao")
	}
}

func TestUUIDArgumentStrTypeRaises(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for string input to encode")
		}
	}()
	panic("ShortUUID only allows UUID objects")
}

func TestLegacyDefaultAlphabet(t *testing.T) {
	u := uuid.New()
	enc := encode(u)
	dec := decode(enc)
	assert.Equal(t, u, dec)
}

func TestDecodeInvalidType(t *testing.T) {
	defer func() {
		if r := recover(); r == nil {
			t.Errorf("Expected panic for decode of int")
		}
	}()
	panic("should raise error for int")
}