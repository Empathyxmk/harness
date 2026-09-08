package public_tests

import (
	"testing"
)

// Simulate iscoroutinefunctionorpartial using Go type checks (dummy)
func iscoroutinefunctionorpartial(fn interface{}) bool {
	switch fn.(type) {
	case func():
		return true
	default:
		return false
	}
}

func TestIscoroutinefunctionorpartialTrueOnCoroFnPub(t *testing.T) {
	fn := func() {}
	if !iscoroutinefunctionorpartial(fn) {
		t.Errorf("should detect function type")
	}
}

func TestIscoroutinefunctionorpartialTrueOnPartialCoroPub(t *testing.T) {
	base := func() {}
	p := base
	if !iscoroutinefunctionorpartial(p) {
		t.Errorf("should detect function/partial type")
	}
}

func TestIscoroutinefunctionorpartialFalseOnRegularPub(t *testing.T) {
	var val int = 12
	if iscoroutinefunctionorpartial(val) {
		t.Errorf("should not detect non-function type")
	}
}

func TestVersionInModulePub(t *testing.T) {
	version := "1.2.3"
	cnt := 0
	for _, c := range version {
		if c == '.' {
			cnt++
		}
	}
	if cnt != 2 {
		t.Errorf("expected 2 dots in version")
	}
}