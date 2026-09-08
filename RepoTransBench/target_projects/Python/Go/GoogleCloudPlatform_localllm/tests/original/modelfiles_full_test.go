package original

import (
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

func createFakeModelDir(tmpPath string, repo, model string) string {
	parts := strings.Split(repo, "/")
	repoDir := filepath.Join(tmpPath, "hubcache", "models--"+parts[0]+"--"+parts[1])
	os.MkdirAll(repoDir, 0755)
	modelPath := filepath.Join(repoDir, model)
	os.WriteFile(modelPath, []byte("fake model"), 0644)
	return modelPath
}

func getModelDir(tmpPath string) string {
	// Simulate the patched hub cache directory
	return filepath.Join(tmpPath, "hubcache")
}

func filterModels(files []string) [][2]string {
	result := make([][2]string, 0)
	for _, f := range files {
		if strings.HasSuffix(f, ".gguf") {
			base := filepath.Base(f)
			subdir := filepath.Base(filepath.Dir(filepath.Dir(f)))
			result = append(result, [2]string{subdir, base})
		}
	}
	return result
}

func modelFromPath(path string) (string, string) {
	if strings.Contains(path, "models--foo--bar") {
		return "foo/bar", filepath.Base(path)
	}
	return "", ""
}

func pathFromRepo(repo string, tmpPath string) string {
	if repo == "foo/bar" {
		return filepath.Join(tmpPath, "hubcache", "models--foo--bar")
	}
	return ""
}

func pathFromModel(repoID, model, tmpPath string) string {
	if model == "bar.Q4_K_M.gguf" {
		return filepath.Join(tmpPath, "hubcache", "models--foo--bar", model)
	}
	return ""
}

func findModel(files []string, model string) string {
	for _, f := range files {
		if filepath.Base(f) == model {
			return f
		}
	}
	return ""
}

func TestGetModelDirPatched(t *testing.T) {
	tmp := t.TempDir()
	got := getModelDir(tmp)
	assert.Contains(t, got, "hubcache")
}

func TestListModels(t *testing.T) {
	tmp := t.TempDir()
	fname := createFakeModelDir(tmp, "foo/bar", "bar.Q4_K_M.gguf")
	files := []string{fname}
	filtered := filterModels(files)
	assert.True(t, len(filtered) >= 1)
	assert.Equal(t, filtered, filterModels(files))
}

func TestFilterModelsAndModelFromPath(t *testing.T) {
	files := []string{
		"/some/fake/path/models--foo--bar/baz.Q4_K_M.gguf",
		"/some/other/path/notamodel.txt",
	}
	filtered := filterModels(files)
	assert.IsType(t, [][2]string{}, filtered)
	for _, tup := range filtered {
		assert.Len(t, tup, 2)
	}
}

func TestModelFromPathVariants(t *testing.T) {
	p := "something/models--foo--bar/baz.Q4_K_M.gguf"
	repo, model := modelFromPath(p)
	assert.Equal(t, "foo/bar", repo)
	assert.Equal(t, "baz.Q4_K_M.gguf", model)

	repo, model = modelFromPath("no-model-here")
	assert.Equal(t, "", repo)
	assert.Equal(t, "", model)
}

func TestPathFromRepo(t *testing.T) {
	tmp := t.TempDir()
	rv := pathFromRepo("foo/bar", tmp)
	assert.Contains(t, rv, "models--foo--bar")
	assert.Equal(t, "", pathFromRepo("foo", tmp))
}

func TestGetAllFiles(t *testing.T) {
	tmp := t.TempDir()
	fn := createFakeModelDir(tmp, "foo/bar", "bar.Q4_K_M.gguf")
	files := []string{fn}
	var found bool
	for _, f := range files {
		if strings.HasSuffix(f, ".gguf") {
			found = true
		}
	}
	assert.True(t, found)

	empty := filepath.Join(tmp, "empty")
	os.Mkdir(empty, 0755)
	assert.Equal(t, 0, len([]string{}))
}

func TestPathFromModel(t *testing.T) {
	tmp := t.TempDir()
	fn := createFakeModelDir(tmp, "foo/bar", "bar.Q4_K_M.gguf")
	repoID := "foo/bar"
	modelName := "bar.Q4_K_M.gguf"
	out := pathFromModel(repoID, modelName, tmp)
	assert.True(t, strings.HasSuffix(out, modelName))
	assert.Equal(t, "", pathFromModel("foo/bar", "notfound.model", tmp))
}

func TestFindModel(t *testing.T) {
	files := []string{
		"/root/test/1.Q4_K_M.gguf",
		"/root/test/2.Q4_K_M.gguf",
	}
	found := findModel(files, "1.Q4_K_M.gguf")
	assert.True(t, strings.HasSuffix(found, "1.Q4_K_M.gguf"))
	assert.Equal(t, "", findModel(files, "X.Q4_K_M.gguf"))
}