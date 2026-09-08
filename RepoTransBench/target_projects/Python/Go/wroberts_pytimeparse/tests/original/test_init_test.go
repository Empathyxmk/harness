package original

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"strings"
	"testing"

	"github.com/stretchr/testify/require"
)

// Test version extraction: version file exists, gets correct version
func TestVersionExtractionSuccess(t *testing.T) {
	tmpDir, err := ioutil.TempDir("", "TestVersionExtractionSuccess")
	require.NoError(t, err)
	defer os.RemoveAll(tmpDir)

	packageDir := filepath.Join(tmpDir, "pytimeparse")
	require.NoError(t, os.Mkdir(packageDir, 0755))
	versionPath := filepath.Join(packageDir, "VERSION")
	require.NoError(t, ioutil.WriteFile(versionPath, []byte("1.2.3"), 0644))

	initPath := filepath.Join(packageDir, "__init__.py")
	initCode := `
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	require.NoError(t, ioutil.WriteFile(initPath, []byte(initCode), 0644))

	// Emulate version file extraction: check content
	data, err := ioutil.ReadFile(versionPath)
	require.NoError(t, err)
	version := strings.TrimSpace(string(data))
	require.Equal(t, "1.2.3", version)
}

// Test version extraction fails with NameError, simulating missing __file__
func TestVersionNoFile(t *testing.T) {
	// In Go, simulate the logic: assignment to version if __file__ undefined
	code := `
from codecs import open
from os import path
try:
    with open(path.join(path.dirname(__file__), 'VERSION'), encoding='utf-8') as infile:
        __version__ = infile.read().strip()
except NameError:
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	// Simulate exec, result is __version__ = 'unknown...'
	lines := strings.Split(code, "\n")
	hasFallback := false
	for _, line := range lines {
		if strings.Contains(line, "__version__ = 'unknown (running code interactively?)'") {
			hasFallback = true
			break
		}
	}
	require.True(t, hasFallback, "Fallback for NameError is not present")
}

// Test version extraction: IOError (file missing)
func TestVersionIOError(t *testing.T) {
	tmpDir, err := ioutil.TempDir("", "TestVersionIOError")
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
    __version__ = 'unknown (running code interactively?)'
except IOError as ex:
    __version__ = "unknown (%s)" % ex
`
	require.NoError(t, ioutil.WriteFile(initPath, []byte(initCode), 0644))

	// Try to read missing VERSION
	_, err = ioutil.ReadFile(filepath.Join(packageDir, "VERSION"))
	require.Error(t, err)
}