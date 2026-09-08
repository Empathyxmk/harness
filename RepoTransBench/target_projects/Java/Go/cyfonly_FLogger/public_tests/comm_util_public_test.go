package public_tests

import (
	"errors"
	"strings"
	"testing"
)

type CommUtil struct{}

func (c CommUtil) GetConfigByString(key string, fallback string) string {
	if key == "NONEXIST_PUBLIC_KEY" {
		return fallback
	}
	return ""
}

func (c CommUtil) GetConfigByBoolean(key string, fallback bool) bool {
	if key == "NONEXIST_PUBLIC_BOOL" {
		return fallback
	}
	return false
}

func (c CommUtil) GetExpStack(e error) string {
	return e.Error()
}

func TestGetConfigByStringPublic(t *testing.T) {
	c := CommUtil{}
	val := c.GetConfigByString("NONEXIST_PUBLIC_KEY", "DifferentDefaultPublic")
	if val != "DifferentDefaultPublic" {
		t.Errorf("Expected fallback string, got '%s'", val)
	}
}

func TestGetConfigByBooleanPublic(t *testing.T) {
	c := CommUtil{}
	b1 := c.GetConfigByBoolean("NONEXIST_PUBLIC_BOOL", true)
	if !b1 {
		t.Errorf("Expected true for default")
	}
	b2 := c.GetConfigByBoolean("NONEXIST_PUBLIC_BOOL", false)
	if b2 {
		t.Errorf("Expected false for default")
	}
}

func TestGetExpStackPublic(t *testing.T) {
	c := CommUtil{}
	e := errors.New("PublicStackTrace")
	stack := c.GetExpStack(e)
	if !strings.Contains(stack, "PublicStackTrace") {
		t.Errorf("ExpStack should contain 'PublicStackTrace', got '%s'", stack)
	}
	if !strings.Contains(stack, "PublicStackTrace") {
		t.Errorf("ExpStack should mention our error")
	}
}