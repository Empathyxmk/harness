package original

import (
    "testing"
    "flashtext"
)

func TestExtractWithSpan(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java")
    kp.AddKeyword("python")

    spanResults := kp.ExtractKeywordSpans("java python java")
    if len(spanResults) != 3 {
        t.Errorf("Expected three spans, got %d", len(spanResults))
    }
}