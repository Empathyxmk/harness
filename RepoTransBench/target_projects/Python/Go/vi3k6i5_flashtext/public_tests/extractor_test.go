package public_tests

import (
    "testing"
    "flashtext"
)

func TestPublicExtractor(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("python")
    kp.AddKeyword("golang")
    res := kp.ExtractKeywords("python is cool; golang is awesome.")
    if len(res) != 2 || res[0] != "python" || res[1] != "golang" {
        t.Errorf("Expected [python golang], got %v", res)
    }
}