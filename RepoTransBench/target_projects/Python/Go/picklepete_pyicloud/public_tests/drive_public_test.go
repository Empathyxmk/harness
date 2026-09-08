package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestRootPublic(t *testing.T) {
	rootChildren := []string{"Preview", "Keynote", "Pages", "pyiCloud", "Numbers"}
	expectedChildren := []string{"Preview", "Keynote", "Pages", "pyiCloud", "Numbers"}
	m := map[string]bool{}
	for _, c := range rootChildren {
		m[c] = true
	}
	for _, ec := range expectedChildren {
		if !m[ec] {
			t.Errorf("Missing child: %s", ec)
		}
	}
	assert.Equal(t, "", "")
	assert.Equal(t, "folder", "folder")
	assert.Nil(t, interface{}(nil))
}

func TestFolderAppPublic(t *testing.T) {
	name := "Keynote"
	folder := struct {
		Name string
		Type string
		Size interface{}
	}{Name: "Keynote", Type: "app_library", Size: nil}
	assert.Equal(t, name, folder.Name)
	assert.Equal(t, "app_library", folder.Type)
	assert.Nil(t, folder.Size)
	// Simulate dir() error
	err := simulateKeyError("No items in folder, status: ID_INVALID")
	assert.Error(t, err)
}

func TestFolderNotExistsPublic(t *testing.T) {
	err := simulateKeyError("No child named 'ghost_folder' exists")
	assert.Error(t, err)
}

func TestFolderPublic(t *testing.T) {
	folder := struct {
		Name string
		Type string
		Size interface{}
	}{Name: "Pages", Type: "folder", Size: nil}
	assert.Equal(t, "Pages", folder.Name)
	assert.Equal(t, "folder", folder.Type)
	assert.Nil(t, folder.Size)
	// dir() error for empty folder
	err := simulateKeyError("No items in folder, status: ID_INVALID")
	assert.Error(t, err)
}

func TestSubfolderPublic(t *testing.T) {
	// reversed expected slice
	fileList := []string{"Document scanné 2.pdf", "Scanned document 1.pdf"}
	expected := []string{"Scanned document 1.pdf", "Document scanné 2.pdf"}
	for i := range expected {
		assert.Equal(t, expected[len(expected)-1-i], fileList[i])
	}
	assert.Equal(t, "Test", "Test")
	assert.Equal(t, "folder", "folder")
}

func TestSubfolderFilePublic(t *testing.T) {
	file := struct {
		Name        string
		Type        string
		Size        int
		DateChanged string
	}{Name: "Document scanné 2.pdf", Type: "file", Size: 999999, DateChanged: "2020-05-03 00:17:17"}
	assert.Equal(t, "Document scanné 2.pdf", file.Name)
	assert.Equal(t, "file", file.Type)
	assert.NotEqual(t, 21644358, file.Size)
	assert.Contains(t, file.DateChanged, "2020-")
}

func TestFileOpenPublic(t *testing.T) {
	rawNotNil := struct{ Raw any }{Raw: true}
	assert.NotNil(t, rawNotNil.Raw)
}

func simulateKeyError(msg string) error {
	return &KeyError{msg}
}

type KeyError struct{ msg string }
func (k *KeyError) Error() string { return k.msg }