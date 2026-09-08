package public_tests

import (
    "testing"
)

func TestMultiplicationIsCorrectPublic(t *testing.T) {
    if 3*5 != 15 {
        t.Errorf("Expected 15, got %d", 3*5)
    }
}