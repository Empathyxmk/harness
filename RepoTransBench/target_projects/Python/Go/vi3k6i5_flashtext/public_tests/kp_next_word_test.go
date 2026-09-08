package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicKPNextWord(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python")
    word, found := kp.NextWord("python golang", 0)
    if !found || word != "python" {
        t.Errorf("Expected first word to be 'python', got '%v'", word)
    }
}