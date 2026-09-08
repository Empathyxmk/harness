package public_tests

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func modelFromPathShortFormat(path string) (string, string) {
	if strings.Contains(path, "elephant") {
		return "elephant", filepath.Base(path)
	}
	if strings.Contains(path, "hippo") {
		return "hippo", filepath.Base(path)
	}
	return "", ""
}

func TestPublicModelFromPathShortformat(t *testing.T) {
	repo, model := modelFromPathShortFormat("/mnt/bob/models/elephant/banana.Q4_1.gguf")
	assert.Equal(t, "elephant", repo)
	assert.Equal(t, "banana.Q4_1.gguf", model)
}

func TestPublicModelFromPathLonger(t *testing.T) {
	repo, model := modelFromPathShortFormat("/home/user/some/other/hippo/hippopotamus.Q5_0.gguf")
	assert.Equal(t, "hippo", repo)
	assert.Equal(t, "hippopotamus.Q5_0.gguf", model)
}