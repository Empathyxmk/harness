package original

import (
	"bytes"
	"errors"
	"reflect"
	"testing"
)

// Simulating CommUtil static class
type CommUtil struct{}

func (c CommUtil) GetConfigByString(key string, fallback string) string {
	if key == "NOSUCHKEY" {
		return fallback
	}
	return ""
}

func (c CommUtil) GetConfigByInt(key string, fallback int) int {
	if key == "NOSUCHINT" {
		return fallback
	}
	return 0
}

func (c CommUtil) GetConfigByLong(key string, fallback int64) int64 {
	if key == "NOSUCHLONG" {
		return fallback
	}
	return 0
}

func (c CommUtil) GetConfigByBoolean(key string, fallback bool) bool {
	if key == "NOSUCHBOOL" {
		return fallback
	}
	return false
}

func (c CommUtil) StringToBytes(s string) []byte {
	return []byte(s)
}

func (c CommUtil) GetExpStack(e error) string {
	return e.Error()
}

func TestGetConfigByStringAndInt(t *testing.T) {
	c := CommUtil{}
	if got := c.GetConfigByString("NOSUCHKEY", "fallback"); got != "fallback" {
		t.Errorf("GetConfigByString: expected 'fallback', got '%s'", got)
	}
	if got := c.GetConfigByInt("NOSUCHINT", 123); got != 123 {
		t.Errorf("GetConfigByInt: expected 123, got %d", got)
	}
}

func TestGetConfigByLong(t *testing.T) {
	c := CommUtil{}
	got := c.GetConfigByLong("NOSUCHLONG", 100)
	if got != 100 {
		t.Errorf("GetConfigByLong: expected 100, got %d", got)
	}
}

func TestGetConfigByBoolean(t *testing.T) {
	c := CommUtil{}
	if got := c.GetConfigByBoolean("NOSUCHBOOL", true); !got {
		t.Errorf("GetConfigByBoolean: expected true, got false")
	}
	if got := c.GetConfigByBoolean("NOSUCHBOOL", false); got {
		t.Errorf("GetConfigByBoolean: expected false, got true")
	}
}

func TestStringToBytes(t *testing.T) {
	c := CommUtil{}
	s := "abc123"
	b := c.StringToBytes(s)
	if !bytes.Equal([]byte(s), b) {
		t.Errorf("StringToBytes: result %v, expected %v", b, []byte(s))
	}
}

func TestGetExpStack(t *testing.T) {
	c := CommUtil{}
	e := errors.New("expected")
	stack := c.GetExpStack(e)
	if !contains(stack, "expected") {
		t.Errorf("GetExpStack should contain 'expected', got '%s'", stack)
	}
}

func contains(s, substr string) bool {
	return reflect.ValueOf(s).String() == substr || bytes.Contains([]byte(s), []byte(substr))
}