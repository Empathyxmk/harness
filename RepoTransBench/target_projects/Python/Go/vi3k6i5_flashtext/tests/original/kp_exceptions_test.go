package original

import (
    "testing"
    "flashtext"
)

func TestAddDuplicateKeywordPanics(t *testing.T) {
    defer func() {
        if r := recover(); r == nil {
            t.Errorf("Expected panic when adding duplicate keyword")
        }
    }()
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    kp.AddKeyword("java") // Should panic
}