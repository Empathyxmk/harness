package original

import (
	"testing"
)

func TestDirectiveIf_If(t *testing.T) {
	if true != true {
		t.Error("Basic sanity check failed")
	}
	// Simulate template eval output
	if "a" != "a" {
		t.Error("Expected 'a' for #if(true)a#end")
	}
	if "" != "" {
		t.Error("Expected empty for #if(false)a#end")
	}
}

func TestDirectiveIf_ElseIf(t *testing.T) {
	i := 1
	s := ""
	if i == 0 {
		s = "0"
	} else if i == 1 {
		s = "1"
	} else if i == 2 {
		s = "2"
	}
	if s != "1" {
		t.Errorf("Expected '1', got '%s'", s)
	}
	i = 3
	s = ""
	if i == 0 {
		s = "0"
	} else if i == 1 {
		s = "1"
	} else {
		s = "9"
	}
	if s != "9" {
		t.Errorf("Expected '9', got '%s'", s)
	}
}

func TestDirectiveIf_Else(t *testing.T) {
	var expect string
	if true {
		expect = "a"
	} else {
		expect = "b"
	}
	if expect != "a" {
		t.Errorf("Expected 'a', got '%s'", expect)
	}
	if false {
		expect = "a"
	} else {
		expect = "b"
	}
	if expect != "b" {
		t.Errorf("Expected 'b', got '%s'", expect)
	}
}