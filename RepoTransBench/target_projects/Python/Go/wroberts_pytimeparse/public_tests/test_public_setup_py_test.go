package public_tests

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestPublicSetupPyRuns(t *testing.T) {
	tmpDir, err := ioutil.TempDir("", "TestPublicSetupPyRuns")
	require.NoError(t, err)
	defer os.RemoveAll(tmpDir)

	projectDir := tmpDir
	pyDir := filepath.Join(projectDir, "pytimeparse")
	err = os.Mkdir(pyDir, 0755)
	require.NoError(t, err)

	err = ioutil.WriteFile(filepath.Join(pyDir, "VERSION"), []byte("2.77"), 0644)
	require.NoError(t, err)
	err = ioutil.WriteFile(filepath.Join(projectDir, "README.rst"), []byte("other longdesc"), 0644)
	require.NoError(t, err)

	setupPath := filepath.Join(projectDir, "setup.py")
	f, err := os.Create(setupPath)
	require.NoError(t, err)
	content := `
from setuptools import setup, find_packages
HERE = "` + projectDir + `"
with open(HERE + "/pytimeparse/VERSION", encoding="utf-8") as f:
    VERSION = f.read().strip()
with open(HERE + "/README.rst", encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()
`
	_, err = f.WriteString(content)
	require.NoError(t, err)
	f.Close()

	_, err = os.Stat(setupPath)
	require.NoError(t, err)
}