package original

import (
    "testing"
)

func TestUtilsAdditionIsCorrect(t *testing.T) {
    if 2+2 != 4 {
        t.Errorf("Expected 4, got %d", 2+2)
    }
}