package public_tests

import "testing"

func TestPublicMiscDummy(t *testing.T) {
	if !(8 < 10) {
		t.Errorf("Expected 8 < 10")
	}
}

func TestPublicMiscOther(t *testing.T) {
	if reverse("XYZ") != "ZYX" {
		t.Errorf("Expected reverse of XYZ to be ZYX")
	}
}

func reverse(s string) string {
	runes := []rune(s)
	for i, j := 0, len(runes)-1; i < j; i, j = i+1, j-1 {
		runes[i], runes[j] = runes[j], runes[i]
	}
	return string(runes)
}