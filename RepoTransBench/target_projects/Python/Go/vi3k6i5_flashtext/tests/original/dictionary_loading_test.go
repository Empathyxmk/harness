package original

import (
    "os"
    "path/filepath"
    "testing"
    "flashtext"
)

func TestDictionaryLoading(t *testing.T) {
    // Setup: create a new KeywordProcessor
    kp := flashtext.NewKeywordProcessor()
    // Load keywords from testdata folder
    absPath, err := filepath.Abs("../testdata/keywords_format_one.txt")
    if err != nil {
        t.Fatalf("failed to resolve absolute path: %v", err)
    }

    count, err := kp.LoadKeywordsFromFile(absPath)
    if err != nil {
        t.Fatalf("failed to load keywords: %v", err)
    }
    if count != 2 {
        t.Errorf("keyword count mismatch: got %d, want %d", count, 2)
    }

    // Test that all keywords are loaded
    if !kp.ContainsKeyword("java") {
        t.Errorf("expected keyword 'java' not found")
    }
    if !kp.ContainsKeyword("python") {
        t.Errorf("expected keyword 'python' not found")
    }
}