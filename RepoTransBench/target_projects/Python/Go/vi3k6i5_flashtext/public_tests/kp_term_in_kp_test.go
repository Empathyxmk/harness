package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicKPContains(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python")
    if !kp.ContainsKeyword("python") {
        t.Error("Should contain 'python'")
    }
    if kp.ContainsKeyword("ruby") {
        t.Error("Should not contain 'ruby'")
    }
}