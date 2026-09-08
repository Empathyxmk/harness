package public_tests

import (
    "testing"
)

func TestSubtractionIsCorrectPublic(t *testing.T) {
    if 8-3 != 5 {
        t.Errorf("Expected 5, got %d", 8-3)
    }
}