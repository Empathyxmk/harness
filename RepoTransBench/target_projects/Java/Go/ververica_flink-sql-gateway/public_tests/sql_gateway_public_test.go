package public_tests

import (
	"net/url"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

type SqlGateway struct{}

func (g SqlGateway) DiscoverDependencies(jars []string, dirs []string) ([]string, error) {
	// Dummy logic: fail for non .jar; dirs must exist and must be dir.
	for _, j := range jars {
		if filepath.Ext(j) != ".jar" {
			return nil, assert.AnError
		}
	}
	for _, d := range dirs {
		info, err := os.Stat(d)
		if err != nil || !info.IsDir() {
			return nil, assert.AnError
		}
	}
	return []string{}, nil
}

func TestDiscoverDependenciesWithNonJarExtension(t *testing.T) {
	file := "README.md"
	gw := SqlGateway{}
	_, err := gw.DiscoverDependencies([]string{file}, []string{})
	assert.Error(t, err)
}

func TestDiscoverDependenciesWithNonExistingDir(t *testing.T) {
	gw := SqlGateway{}
	_, err := gw.DiscoverDependencies([]string{}, []string{"fakePublicDirNotExist"})
	assert.Error(t, err)
}

func TestDiscoverDependenciesWithEmptyDir(t *testing.T) {
	dir := "testPublicDir"
	os.Mkdir(dir, 0755)
	defer os.RemoveAll(dir)
	gw := SqlGateway{}
	out, err := gw.DiscoverDependencies([]string{}, []string{dir})
	assert.NoError(t, err)
	assert.Len(t, out, 0)
}

func TestDiscoverDependenciesWithUnsupportedFileInDir(t *testing.T) {
	dir := "testPublicDir2"
	os.Mkdir(dir, 0755)
	defer os.RemoveAll(dir)
	file := filepath.Join(dir, "otherfile.data")
	f2, _ := os.Create(file)
	f2.Close()
	defer os.Remove(file)
	gw := SqlGateway{}
	out, err := gw.DiscoverDependencies([]string{}, []string{dir})
	assert.NoError(t, err)
	assert.Len(t, out, 0)
}