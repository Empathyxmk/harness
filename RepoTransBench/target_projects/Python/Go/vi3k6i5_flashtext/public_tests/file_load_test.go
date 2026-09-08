package public_tests

import (
    "testing"
    "flashtext"
    "path/filepath"
)

func TestPublicFileLoad(t *testing.T) {
    kp := flashtext.NewKeywordProcessor()
    p, err := filepath.Abs("../tests/testdata/keywords_format_two.txt")
    if err != nil {
        t.Fatalf("Failed to get absolute path: %v", err)
    }
    n, err := kp.LoadKeywordsFromFile(p)
    if err != nil || n != 3 {
        t.Errorf("Failed to load 3 keywords, got %d, err %v", n, err)
    }
}