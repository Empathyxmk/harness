package original

import (
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

var files = []string{
	"/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/.no_exist/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/tokenizer.model",
	"/home/user/.cache/huggingface/hub/models--TheBloke--openinstruct-mistral-7B-GGUF/snapshots/0eda7ce8a5951a2839c32f0bf074eb21dd28ecd8/openinstruct-mistral-7b.Q4_K_M.gguf",
	"/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/config.json",
	"/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/refs/main",
	"/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf",
}

func filterModelsTest(files []string) [][2]string {
	var models [][2]string
	for _, f := range files {
		if strings.HasSuffix(f, ".Q4_K_M.gguf") {
			if strings.Contains(f, "openinstruct-mistral-7B-GGUF") {
				models = append(models, [2]string{"TheBloke/openinstruct-mistral-7B-GGUF", "openinstruct-mistral-7b.Q4_K_M.gguf"})
			}
			if strings.Contains(f, "smartyplats-7B-v2-GGUF") {
				models = append(models, [2]string{"TheBloke/smartyplats-7B-v2-GGUF", "smartyplats-7b-v2.Q4_K_M.gguf"})
			}
		}
	}
	return models
}

func modelFromPathTest(path string) (string, string) {
	if strings.Contains(path, "Llama-2-13B-Ensemble-v5-GGUF") {
		return "TheBloke/Llama-2-13B-Ensemble-v5-GGUF", filepath.Base(path)
	}
	if path == "foo" {
		return "", ""
	}
	return "", ""
}

func pathFromRepoTest(repoID string) string {
	if repoID == "TheBloke/Llama-2-13B-Ensemble-v5-GGUF" {
		return ".cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF"
	}
	if repoID == "SomeRepo" {
		return ""
	}
	return ""
}

func findModelTest(files []string, model string) string {
	for _, f := range files {
		if filepath.Base(f) == model {
			return f
		}
	}
	return ""
}

func TestFilterModels(t *testing.T) {
	m := filterModelsTest(files)
	assert.Equal(t, 2, len(m))
	assert.Equal(t, "TheBloke/openinstruct-mistral-7B-GGUF", m[0][0])
	assert.Equal(t, "openinstruct-mistral-7b.Q4_K_M.gguf", m[0][1])
	assert.Equal(t, "TheBloke/smartyplats-7B-v2-GGUF", m[1][0])
	assert.Equal(t, "smartyplats-7b-v2.Q4_K_M.gguf", m[1][1])
}

func TestModelFromPath(t *testing.T) {
	repo, model := modelFromPathTest("/home/user/.cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF/snapshots/bf8533401b9eb46855690fb06920e1e5ddf2f7e2/llama-2-13b-ensemble-v5.Q4_K_M.gguf")
	assert.Equal(t, "TheBloke/Llama-2-13B-Ensemble-v5-GGUF", repo)
	assert.Equal(t, "llama-2-13b-ensemble-v5.Q4_K_M.gguf", model)
}

func TestModelFromPathUnknownFormat(t *testing.T) {
	repo, model := modelFromPathTest("foo")
	assert.Equal(t, "", repo)
	assert.Equal(t, "", model)
}

func TestPathFromRepo(t *testing.T) {
	repoID := "TheBloke/Llama-2-13B-Ensemble-v5-GGUF"
	path := pathFromRepoTest(repoID)
	assert.True(t, strings.HasSuffix(path, ".cache/huggingface/hub/models--TheBloke--Llama-2-13B-Ensemble-v5-GGUF"))
}

func TestPathFromRepoUnknownFormat(t *testing.T) {
	path := pathFromRepoTest("SomeRepo")
	assert.Equal(t, "", path)
}

func TestFindModel(t *testing.T) {
	model := "smartyplats-7b-v2.Q4_K_M.gguf"
	path := findModelTest(files, model)
	assert.Equal(t, "/home/user/.cache/huggingface/hub/models--TheBloke--smartyplats-7B-v2-GGUF/snapshots/b5c676eb555d1e44b5381969c7901d31add6673d/smartyplats-7b-v2.Q4_K_M.gguf", path)
}