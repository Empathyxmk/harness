package original

import (
    "testing"
    "flashtext"
)

func TestKeywordProcessorLen(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    if l := kp.Len(); l != 0 {
        t.Errorf("initial length should be 0, got %d", l)
    }
    kp.AddKeyword("java")
    if l := kp.Len(); l != 1 {
        t.Errorf("after adding a keyword, length should be 1, got %d", l)
    }
}