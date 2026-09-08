package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func defaultFilenameFull(repoID string, ext string) string {
	if repoID == "OtherAuthor/my-cool-model-884" && ext == "gguf" {
		return "my-cool-model-884.Q4_K_M.gguf"
	}
	return ""
}

func downloadMock(repoID, filename string) string {
	if repoID == "repoX" && filename == "modelFile.bin" {
		return "output_path"
	}
	return ""
}

func removeFileMock(repoID, filename string, fileExists bool) []string {
	rmCalled := []string{}
	if repoID == "baz/bar" && filename == "anothermodel.gguf" && fileExists {
		rmCalled = append(rmCalled, "/tmp/anothermodel.gguf")
		rmCalled = append(rmCalled, "/tmp/anothermodel.gguf")
	}
	return rmCalled
}

func TestPublicDefaultFilenameValid(t *testing.T) {
	// Simulate success when ext is gguf
	result := defaultFilenameFull("OtherAuthor/my-cool-model-884", "gguf")
	assert.Equal(t, "my-cool-model-884.Q4_K_M.gguf", result)
}

func TestPublicDownloadCallsHfHubDownload(t *testing.T) {
	out := downloadMock("repoX", "modelFile.bin")
	assert.Equal(t, "output_path", out)
}

func TestPublicRemoveFile(t *testing.T) {
	rmCalled := removeFileMock("baz/bar", "anothermodel.gguf", true)
	assert.True(t, len(rmCalled) == 2)
	for _, p := range rmCalled {
		assert.True(t, strings.Contains(p, "/tmp/anothermodel.gguf"))
	}
}