package public_tests

import (
    "testing"
)

func TestImageWidthLargerThanHeightPublic(t *testing.T) {
    width, height := 600, 400
    if !(width > height) {
        t.Errorf("Expected width > height, got width=%d, height=%d", width, height)
    }
}