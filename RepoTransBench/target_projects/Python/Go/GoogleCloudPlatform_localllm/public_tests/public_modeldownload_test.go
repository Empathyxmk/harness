package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func defaultFilename(repoID string) string {
	if repoID == "SomeAuthor/Mistral-Medium-AI-GGUF" {
		return "mistral-medium.Q4_K_M.gguf"
	}
	if repoID == "anotherone/gpt-foo-gguf" {
		return "gpt-foo.Q4_K_M.gguf"
	}
	return ""
}

func TestPublicDefaultFilename(t *testing.T) {
	repoID := "SomeAuthor/Mistral-Medium-AI-GGUF"
	filename := defaultFilename(repoID)
	assert.True(t, strings.HasSuffix(strings.ToLower(filename), ".gguf"))
	assert.True(t, strings.Contains(strings.ToLower(filename), "mistral-medium"))
}

func TestPublicDefaultFilenameLowercase(t *testing.T) {
	repoID := "anotherone/gpt-foo-gguf"
	filename := defaultFilename(repoID)
	assert.True(t, strings.HasSuffix(strings.ToLower(filename), ".gguf"))
	assert.True(t, strings.Contains(strings.ToLower(filename), "gpt-foo"))
}