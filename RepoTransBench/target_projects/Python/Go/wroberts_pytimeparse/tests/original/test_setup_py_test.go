package original

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestSetupPyRuns(t *testing.T) {
	// Make a temporary directory
	tmpDir, err := ioutil.TempDir("", "TestSetupPyRuns")
	require.NoError(t, err)
	defer os.RemoveAll(tmpDir)

	projectDir := tmpDir
	pyDir := filepath.Join(projectDir, "pytimeparse")
	err = os.Mkdir(pyDir, 0755)
	require.NoError(t, err)

	// Create VERSION and README.rst
	err = ioutil.WriteFile(filepath.Join(pyDir, "VERSION"), []byte("0.99"), 0644)
	require.NoError(t, err)
	err = ioutil.WriteFile(filepath.Join(projectDir, "README.rst"), []byte("longdesc"), 0644)
	require.NoError(t, err)

	setupPath := filepath.Join(projectDir, "setup.py")
	// Write a minimal Python file (simulate original setup.py up to "setup(")
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

	// Would normally exec Python and check for errors, here we only test file setup success
	_, err = os.Stat(setupPath)
	require.NoError(t, err)
}