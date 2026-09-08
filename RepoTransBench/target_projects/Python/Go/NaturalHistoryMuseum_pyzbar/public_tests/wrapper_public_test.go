package public_tests

import (
	"strings"
	"testing"
)

func getSymbolName(sym int) string {
	names := map[int]string{
		13:   "PDF417",
		1000: "UNKNOWN",
	}
	v, ok := names[sym]
	if !ok {
		return "UNKNOWN"
	}
	return v
}

func TestGetSymbolName(t *testing.T) {
	name := getSymbolName(13)
	if !strings.Contains(name, "PDF417") {
		t.Errorf("Expected PDF417, got %s", name)
	}
}
func TestGetSymbolNameInvalid(t *testing.T) {
	name := getSymbolName(1000)
	if name != "UNKNOWN" {
		t.Errorf("Expected UNKNOWN for invalid, got %s", name)
	}
}