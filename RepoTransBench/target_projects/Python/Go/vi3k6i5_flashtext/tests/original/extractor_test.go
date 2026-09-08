package original

import (
    "testing"
    "flashtext"
)

func TestExtractor(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    kp.AddKeyword("python")

    res := kp.ExtractKeywords("I love java and python")
    if len(res) != 2 || res[0] != "java" || res[1] != "python" {
        t.Errorf("expected [java python], got %v", res)
    }
}