package original

import (
	"io/ioutil"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

type SetupMod struct{}

func (SetupMod) Read(fname string) (string, error) {
	b, err := ioutil.ReadFile(fname)
	if err != nil {
		return "", err
	}
	return string(b), nil
}

func TestReadSuccess(t *testing.T) {
	tmpDir := t.TempDir()
	filename := filepath.Join(tmpDir, "afile")
	err := ioutil.WriteFile(filename, []byte("DATA"), 0644)
	assert.NoError(t, err)
	setupmod := SetupMod{}
	data, err := setupmod.Read(filename)
	assert.NoError(t, err)
	assert.Equal(t, "DATA", data)
}

func TestReadFileNotFound(t *testing.T) {
	setupmod := SetupMod{}
	_, err := setupmod.Read("idonotexist.txt")
	assert.Error(t, err)
}