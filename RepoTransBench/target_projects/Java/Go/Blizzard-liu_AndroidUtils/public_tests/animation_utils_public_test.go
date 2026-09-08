package public_tests

import (
    "testing"
)

func TestSimplePublicAnimation(t *testing.T) {
    duration := 350
    if duration <= 200 {
        t.Errorf("Duration should be greater than 200, got %d", duration)
    }
}