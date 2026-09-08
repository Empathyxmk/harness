package public_tests

import (
    "testing"
    "twigmodule/tests"
)

func TestConstructorDifferentNamePublic(t *testing.T) {
    item := tests.NewTwigStructureItem("otherPublicName", "block", 7, 12)
    if item.GetName() != "otherPublicName" {
        t.Errorf("Expected name 'otherPublicName', got '%v'", item.GetName())
    }
    if item.GetKind() != "block" {
        t.Errorf("Expected kind 'block', got '%v'", item.GetKind())
    }
    if item.GetOffset() != 7 {
        t.Errorf("Expected offset 7, got %d", item.GetOffset())
    }
    if item.GetEndOffset() != 12 {
        t.Errorf("Expected endOffset 12, got %d", item.GetEndOffset())
    }
}