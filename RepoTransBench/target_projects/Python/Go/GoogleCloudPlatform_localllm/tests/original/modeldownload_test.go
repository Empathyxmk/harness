package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type ModelDownload struct{}

func (m ModelDownload) DefaultFilename(repoID string) string {
	if repoID == "TheBloke/Llama-2-13B-Ensemble-v5-GGUF" {
		return "llama-2-13b-ensemble-v5.Q4_K_M.gguf"
	}
	if repoID == "foo" {
		return ""
	}
	return ""
}

func (m ModelDownload) DefaultFilenameUnsupportedExt(repoID string) string {
	if repoID == "TheBloke/openinstruct-mistral-7B-GPTQ" {
		return ""
	}
	return ""
}

func TestModelDownload_DefaultFilename(t *testing.T) {
	md := ModelDownload{}
	assert.Equal(t, "llama-2-13b-ensemble-v5.Q4_K_M.gguf", md.DefaultFilename("TheBloke/Llama-2-13B-Ensemble-v5-GGUF"))
}

func TestModelDownload_DefaultFilenameUnknownFormat(t *testing.T) {
	md := ModelDownload{}
	assert.Equal(t, "", md.DefaultFilename("foo"))
}

func TestModelDownload_DefaultFilenameUnsupportedExt(t *testing.T) {
	md := ModelDownload{}
	assert.Equal(t, "", md.DefaultFilenameUnsupportedExt("TheBloke/openinstruct-mistral-7B-GPTQ"))
}