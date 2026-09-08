package login

import (
	"testing"
)

func TestMultiplyIsCorrect(t *testing.T) {
	if 5*6 != 30 {
		t.Errorf("Expected 30, got %d", 5*6)
	}
}

func TestStringNotEqualsIsCorrect(t *testing.T) {
	if "login" == "public_login" {
		t.Error(`Expected "login" and "public_login" to be not equal`)
	}
}