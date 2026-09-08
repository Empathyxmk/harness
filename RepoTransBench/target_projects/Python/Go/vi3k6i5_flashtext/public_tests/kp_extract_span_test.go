package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicKPExtractSpan(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("golang")
    kp.AddKeyword("python")

    spans := kp.ExtractKeywordSpans("scalar golang and python code")
    if len(spans) != 2 {
        t.Errorf("Expected 2 spans, got %d", len(spans))
    }
    if spans[0].Keyword != "golang" || spans[1].Keyword != "python" {
        t.Errorf("Unexpected keywords in spans: %+v", spans)
    }
}