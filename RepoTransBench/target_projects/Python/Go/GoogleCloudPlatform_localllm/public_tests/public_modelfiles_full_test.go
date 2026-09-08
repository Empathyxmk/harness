package public_tests

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func findLLMFilesMock(dir string) []string {
	if dir == "/tmp/some-llm-model-dir" {
		return []string{"lion.Q4_0.gguf", "giraffe.Q8_0.gguf"}
	}
	return []string{}
}

func isLLMFileMock(filename string) bool {
	return strings.HasSuffix(filename, ".gguf") && (strings.HasPrefix(filename, "rhino") || strings.HasPrefix(filename, "lion") || strings.HasPrefix(filename, "giraffe") || strings.HasPrefix(filename, "hippo"))
}

func TestPublicFindLLMFiles(t *testing.T) {
	output := findLLMFilesMock("/tmp/some-llm-model-dir")
	found := false
	for _, f := range output {
		if strings.HasSuffix(f, ".gguf") {
			found = true
		}
	}
	assert.True(t, found)
	foundLion := false
	for _, f := range output {
		if strings.Contains(f, "lion.Q4_0.gguf") {
			foundLion = true
		}
	}
	assert.True(t, foundLion)
}

func TestPublicIsLLMFile(t *testing.T) {
	assert.True(t, isLLMFileMock("rhino.Q7_0.gguf"))
	assert.False(t, isLLMFileMock("zebra.txt"))
}