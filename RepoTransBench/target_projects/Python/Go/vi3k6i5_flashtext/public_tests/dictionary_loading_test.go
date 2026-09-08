package public_tests

import (
    "path/filepath"
    "testing"
    "flashtext"
)

func TestPublicDictionaryLoading(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    p, err := filepath.Abs("../tests/testdata/keywords_format_two.txt")
    if err != nil {
        t.Fatalf("Failed to resolve keywords testdata: %v", err)
    }
    count, err := kp.LoadKeywordsFromFile(p)
    if err != nil {
        t.Errorf("Error loading keywords: %v", err)
    }
    if count != 3 {
        t.Errorf("Expected to load 3 keywords, got %d", count)
    }
    if !kp.ContainsKeyword("golang") {
        t.Error("Keyword 'golang' not found in loaded keywords")
    }
    if !kp.ContainsKeyword("java") {
        t.Error("Keyword 'java' not found in loaded keywords")
    }
    if !kp.ContainsKeyword("python") {
        t.Error("Keyword 'python' not found in loaded keywords")
    }
}