package original

import (
    "testing"
    "flashtext"
)

func TestExtractFuzzy(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    kp.AddKeyword("java script", "javascript")
    kp.AddKeyword("javascript", "javascript")
    kp.AddKeyword("java", "java")

    // Test with fuzziness (Assuming a method ExtractFuzzySimilar exists)
    res := kp.ExtractFuzzy("I like javascipt", 2)
    if len(res) == 0 || res[0] != "javascript" {
        t.Errorf("expected 'javascript', got %v", res)
    }

    res = kp.ExtractFuzzy("I like jaba", 2)
    if len(res) == 0 || res[0] != "java" {
        t.Errorf("expected 'java', got %v", res)
    }
}