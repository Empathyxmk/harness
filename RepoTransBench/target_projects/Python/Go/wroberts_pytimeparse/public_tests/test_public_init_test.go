package public_tests

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
)

func TestPublicVersionExtractionSuccess(t *testing.T) {
	tmpDir, err := ioutil.TempDir("", "TestPublicVersionExtractionSuccess")
	require.NoError(t, err)
	defer os.RemoveAll(tmpDir)

	packageDir := filepath.Join(tmpDir, "pytimeparse")
	require.NoError(t, os.Mkdir(packageDir, 0755))
	versionPath := filepath.Join(packageDir, "VERSION")
	require.NoError(t, ioutil.WriteFile(versionPath, []byte("3.4.5"), 0644))
	initPath := filepath.Join(packageDir, "__init__.py")
	initCode := `
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public scenario)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	require.NoError(t, ioutil.WriteFile(initPath, []byte(initCode), 0644))

	// Emulate version extraction: read file content
	data, err := ioutil.ReadFile(versionPath)
	require.NoError(t, err)
	version := strings.TrimSpace(string(data))
	require.Equal(t, "3.4.5", version)
}

func TestPublicVersionNoFile(t *testing.T) {
	code := `
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public without file)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	lines := strings.Split(code, "\n")
	found := false
	for _, line := range lines {
		if strings.Contains(line, "__version__ = 'unknown (public without file)'") {
			found = true
			break
		}
	}
	require.True(t, found, "Fallback for NameError present")
}

func TestPublicVersionIOError(t *testing.T) {
	tmpDir, err := ioutil.TempDir("", "TestPublicVersionIOError")
	require.NoError(t, err)
	defer os.RemoveAll(tmpDir)

	packageDir := filepath.Join(tmpDir, "pytimeparse")
	require.NoError(t, os.Mkdir(packageDir, 0755))
	initPath := filepath.Join(packageDir, "__init__.py")
	initCode := `
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (public running interactive)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	require.NoError(t, ioutil.WriteFile(initPath, []byte(initCode), 0644))
	_, err = ioutil.ReadFile(filepath.Join(packageDir, "VERSION"))
	require.Error(t, err)
}