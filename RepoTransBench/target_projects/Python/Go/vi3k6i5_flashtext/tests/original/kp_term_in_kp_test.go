package original

import (
    "testing"
    "flashtext"
)

func TestKeywordProcessorHasKeyword(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    if !kp.ContainsKeyword("java") {
        t.Errorf("keyword processor should contain 'java'")
    }
    if kp.ContainsKeyword("python") {
        t.Errorf("'python' should not be present")
    }
}