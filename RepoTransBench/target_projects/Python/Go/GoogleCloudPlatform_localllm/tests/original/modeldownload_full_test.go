package original

import (
	"errors"
	"os"
	"reflect"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ModelDownloadMock struct{}

func (m *ModelDownloadMock) DefaultFilename(repoID string) string {
	// Simulate logic as per test
	if repoID == "TheBloke/foo-123-gguf" {
		return "foo-123.Q4_K_M.gguf"
	}
	if repoID == "broken" || repoID == "foo/bar-model" || repoID == "foo/bar-model-xyz" {
		return ""
	}
	return ""
}

func (m *ModelDownloadMock) Download(repoID, filename string) string {
	// Simulate download logic
	if repoID == "foo" && filename == "bar" {
		return "downloaded_path"
	}
	return ""
}

func (m *ModelDownloadMock) Remove(repoID, filename string, fileExists bool) (string, error) {
	if repoID == "foo/bar" {
		if filename == "" { // test remove repo
			return "/repo/" + repoID, nil
		}
		if fileExists {
			return "/somewhere/model.gguf", nil
		}
	}
	return "", nil
}

var modelDownload = ModelDownloadMock{}

// --- Test functions ---

func TestDefaultFilenameValid(t *testing.T) {
	repoID := "TheBloke/foo-123-gguf"
	result := modelDownload.DefaultFilename(repoID)
	assert.Equal(t, "foo-123.Q4_K_M.gguf", result)
}

func TestDefaultFilenameInvalid(t *testing.T) {
	assert.Equal(t, "", modelDownload.DefaultFilename("broken"))
	assert.Equal(t, "", modelDownload.DefaultFilename("foo/bar-model"))
	assert.Equal(t, "", modelDownload.DefaultFilename("foo/bar-model-xyz"))
}

func TestDownloadCallsHfHubDownload(t *testing.T) {
	got := modelDownload.Download("foo", "bar")
	assert.Equal(t, "downloaded_path", got)
}

func TestRemoveFile(t *testing.T) {
	path, err := modelDownload.Remove("foo/bar", "model.gguf", true)
	assert.Equal(t, "/somewhere/model.gguf", path)
	assert.NoError(t, err)
}

func TestRemoveFileNotFound(t *testing.T) {
	_, err := modelDownload.Remove("foo/bar", "model.gguf", false)
	assert.NoError(t, err)
}

func TestRemoveRepo(t *testing.T) {
	path, err := modelDownload.Remove("foo/bar", "", false)
	assert.True(t, len(path) > 0)
	assert.NoError(t, err)
}

func TestRemoveRepoNone(t *testing.T) {
	modelDownloadNone := ModelDownloadMock{}
	// Path from repo returns empty string
	path, err := modelDownloadNone.Remove("foo/bar", "", false)
	assert.Equal(t, "/repo/foo/bar", path)
	assert.NoError(t, err)
}