package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicExceptionOnDuplicateKeyword(t *testing.T) {
    defer func() {
        if recover() == nil {
            t.Error("Expected panic on duplicate keyword")
        }
    }()
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python")
    kp.AddKeyword("python") // Should panic
}