package original

import (
    "testing"
    "flashtext"
)

func TestNextWord(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    word, found := kp.NextWord("java python", 0)
    if !found || word != "java" {
        t.Errorf("expected first word to be 'java', found %v", word)
    }
}