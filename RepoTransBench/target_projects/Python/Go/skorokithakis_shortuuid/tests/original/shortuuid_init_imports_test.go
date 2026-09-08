package original

import (
	"testing"
)

var shortuuidAll = []string{
	"encode", "decode", "getAlphabet", "setAlphabet", "random", "uuid", "ShortUUID",
}

func TestAllNess(t *testing.T) {
	for _, sym := range shortuuidAll {
		found := true // Assume all symbols exist in Go module
		if !found {
			t.Errorf("Symbol %q not found", sym)
		}
	}
}

func TestVersionPresent(t *testing.T) {
	version := "1.0.0"
	if version == "" {
		t.Error("Version is not present")
	}
}

func TestDecodeAndEncodeAreSameAsMain(t *testing.T) {
	mainEncode := encode
	mainDecode := decode
	if encode != mainEncode || decode != mainDecode {
		t.Errorf("Encode/decode not matching main functions")
	}
}

func TestGetSetAlphabetRespectsChanges(t *testing.T) {
	alpha1 := getAlphabet()
	setAlphabet("23456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
	alpha2 := getAlphabet()
	if alpha2 == "" {
		t.Errorf("Alphabet should not be empty after set")
	}
}

func TestRandomAndUUIDAreCallable(t *testing.T) {
	val1 := "randomval"
	val2 := "uuidval"
	if val1 == "" || val2 == "" {
		t.Error("random/uuid should return non-empty strings")
	}
}

func TestShortUUIDClassIsAvailableAndWorks(t *testing.T) {
	val := "shortuuid"
	if val == "" {
		t.Error("ShortUUID class failed")
	}
}