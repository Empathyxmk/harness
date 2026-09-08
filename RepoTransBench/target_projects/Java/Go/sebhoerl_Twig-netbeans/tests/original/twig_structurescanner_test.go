package original

import (
	"testing"
	"twigmodule/tests"
)

func TestScanReturnsTopLevelBlocksOnly(t *testing.T) {
	scanner := tests.NewTwigStructureScanner()
	items := scanner.Scan("")
	if items == nil {
		t.Errorf("Scan returned nil, expected slice")
	}
}

func TestGetHeaderReturnsNull(t *testing.T) {
	scanner := tests.NewTwigStructureScanner()
	if scanner.GetHeader("") != nil {
		t.Error("Expected nil header")
	}
}