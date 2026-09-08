package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicKPLen(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    if kp.Len() != 0 {
        t.Errorf("Length should be 0, got %d", kp.Len())
    }
    kp.AddKeyword("python")
    if kp.Len() != 1 {
        t.Errorf("Length should be 1 after adding, got %d", kp.Len())
    }
}