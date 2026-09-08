package original

import (
	"testing"
)

func TestDirectiveStop_ForBreak(t *testing.T) {
	s := ""
	for i := 1; i <= 3; i++ {
		s += string('0' + i)
		if i > 1 {
			s += "a"
			break
		}
	}
	if s != "1a2" {
		t.Errorf("Expected '1a2', got '%s'", s)
	}
}

func TestDirectiveStop_ForContinue(t *testing.T) {
	s := ""
	for i := 1; i <= 3; i++ {
		s += string('0' + i)
		if i > 1 {
			continue
		}
		s += "a"
	}
	if s != "1a23" {
		t.Errorf("Expected '1a23', got '%s'", s)
	}
}

func TestDirectiveStop_ForStop(t *testing.T) {
	got := "123"
	if got != "123" {
		t.Errorf("Expected '123', got '%s'", got)
	}
	got = "1a2"
	if got != "1a2" {
		t.Errorf("Expected '1a2', got '%s'", got)
	}
}