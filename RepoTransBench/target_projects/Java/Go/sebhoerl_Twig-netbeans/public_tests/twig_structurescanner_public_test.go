package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestScanEmptyReturnsListPublic(t *testing.T) {
    scanner := tests.NewTwigStructureScanner()
    items := scanner.Scan("")
    if items == nil {
        t.Error("Scan should not return nil")
    }
    if len(items) != 0 {
        t.Errorf("Expected empty scan for input '', got %v", items)
    }
}

func TestGetHeaderReturnsNullPublic(t *testing.T) {
    scanner := tests.NewTwigStructureScanner()
    if scanner.GetHeader("") != nil {
        t.Error("Expected nil header")
    }
}