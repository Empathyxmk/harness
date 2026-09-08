package original

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestConfigCmd_FinalizeOptions(t *testing.T) {
	includeDirs := "one" + string(os.PathListSeparator) + "two"
	libraries := "one"
	libraryDirs := "three" + string(os.PathListSeparator) + "four"

	assert.Equal(t, "one"+string(os.PathListSeparator)+"two", includeDirs)
	assert.Equal(t, "one", libraries)
	assert.Equal(t, "three"+string(os.PathListSeparator)+"four", libraryDirs)
}

func TestConfigCmd_Clean(t *testing.T) {
	tDir := t.TempDir()
	f1 := tDir + "/one"
	f2 := tDir + "/two"
	err := os.WriteFile(f1, []byte("xxx"), 0644)
	assert.NoError(t, err)
	err = os.WriteFile(f2, []byte("xxx"), 0644)
	assert.NoError(t, err)
	assert.FileExists(t, f1)
	assert.FileExists(t, f2)

	err = os.Remove(f1)
	assert.NoError(t, err)
	err = os.Remove(f2)
	assert.NoError(t, err)
	assert.NoFileExists(t, f1)
	assert.NoFileExists(t, f2)
}