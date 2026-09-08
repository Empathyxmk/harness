package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicReplacer(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python", "🐍")
    kp.AddKeyword("golang", "🦫")

    s := "python golang"
    replaced := kp.ReplaceKeywords(s)
    if replaced != "🐍 🦫" {
        t.Errorf("Expected '🐍 🦫', got '%v'", replaced)
    }
}