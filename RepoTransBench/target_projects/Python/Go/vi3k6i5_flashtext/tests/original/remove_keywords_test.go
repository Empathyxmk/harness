package original

import (
    "testing"
    "flashtext"
)

func TestRemoveKeywords(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    kp.AddKeyword("python")
    kp.RemoveKeyword("java")
    if kp.ContainsKeyword("java") {
        t.Errorf("'java' should have been removed")
    }
    if !kp.ContainsKeyword("python") {
        t.Errorf("'python' should exist")
    }
}