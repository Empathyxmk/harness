package original

import (
	"path/filepath"
	"runtime"
	"strings"
	"testing"

	"antiboredom_audiogrep/audiogrep"
)

func TestConvertTimestamps(t *testing.T) {
	_, thisfile, _, _ := runtime.Caller(0)
	thisdir := filepath.Dir(thisfile)
	filename := filepath.Join(thisdir, "data", "test.mp3")
	sentences, err := audiogrep.ConvertTimestamps([]string{filename})
	if err != nil {
		t.Fatalf("ConvertTimestamps failed: %v", err)
	}
	words := map[string]bool{}
	for _, sentence := range sentences {
		for _, word := range sentence.Words {
			words[word[0]] = true
		}
	}
	if !words["fashion"] {
		t.Errorf("Expected word 'fashion' not found in words: %v", words)
	}
	if len(sentences) != 9 {
		t.Errorf("Expected 9 sentences, got %d", len(sentences))
	}
}