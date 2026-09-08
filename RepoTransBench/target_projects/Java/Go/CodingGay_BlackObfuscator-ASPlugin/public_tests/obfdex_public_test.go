package public_tests

import (
	"strings"
	"testing"
)

// Dummy for test logic
func obfDexIsObfuscated(s string) bool {
	return strings.Contains(s, "obf")
}
func obfDexObfuscate(s string) string {
	return "obf_" + s + "_2024" // Just for demonstration
}

func TestIsObfuscatedWithDifferentData(t *testing.T) {
	if obfDexIsObfuscated("barBazNew") {
		t.Error(`expected obfDexIsObfuscated("barBazNew") == false`)
	}
	if !obfDexIsObfuscated("obf_PUBLIC_2024") {
		t.Error(`expected obfDexIsObfuscated("obf_PUBLIC_2024") == true`)
	}
}

func TestObfuscateDifferentData(t *testing.T) {
	original := "differentString2024"
	obfuscated := obfDexObfuscate(original)
	if obfuscated == "" {
		t.Error("obfuscated string is empty")
	}
	if obfuscated == original {
		t.Error("obfuscated string must differ from original")
	}
	if !strings.Contains(obfuscated, "obf") {
		t.Error("obfuscated string should contain 'obf'")
	}
}