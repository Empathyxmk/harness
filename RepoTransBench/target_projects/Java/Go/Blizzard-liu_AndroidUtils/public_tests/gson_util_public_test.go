package public_tests

import (
    "strconv"
    "testing"
)

func TestNumberStringDeserializationPublic(t *testing.T) {
    json := "123"
    num, err := strconv.Atoi(json)
    if err != nil {
        t.Fatalf("Failed to parse integer: %v", err)
    }
    if num != 123 {
        t.Errorf("Expected 123, got %d", num)
    }
}