package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicRemoveKeywords(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python")
    kp.AddKeyword("golang")
    kp.RemoveKeyword("python")
    if kp.ContainsKeyword("python") {
        t.Error("python should have been removed")
    }
    if !kp.ContainsKeyword("golang") {
        t.Error("golang should still exist")
    }
}