package original

import (
    "os"
    "path/filepath"
    "testing"
    "flashtext"
)

func TestFileLoad(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    fPath, err := filepath.Abs("../testdata/keywords_format_one.txt")
    if err != nil {
        t.Fatalf("failed to resolve keywords file: %v", err)
    }
    count, err := kp.LoadKeywordsFromFile(fPath)
    if err != nil {
        t.Fatalf("failed to load keywords: %v", err)
    }
    if count != 2 {
        t.Errorf("expected count 2, got %d", count)
    }
}