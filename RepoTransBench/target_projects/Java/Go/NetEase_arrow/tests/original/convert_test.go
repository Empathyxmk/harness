package tests

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulates the "ConvertTest" logic. We do not have Java's Convert.main,
// but we reproduce its essential file encoding conversion behavior here.

func TestConvertGbkToUtf8InPlace(t *testing.T) {
	gbkFile, err := os.CreateTemp("", "testfile*.txt")
	assert.NoError(t, err)
	defer os.Remove(gbkFile.Name())

	utf8File, err := os.CreateTemp("", "utf8file*.txt")
	assert.NoError(t, err)
	defer os.Remove(utf8File.Name())

	// Write Chinese "你好" in GBK encoding
	err = WriteGBKFile(gbkFile.Name(), "你好")
	assert.NoError(t, err)
	RemoveIfExists(utf8File.Name(), t)

	// Convert in-place: simulate Convert.main([gbkFile])
	err = ConvertFileInPlaceGbkToUtf8(gbkFile.Name())
	assert.NoError(t, err)

	content, err := ReadUTF8File(gbkFile.Name())
	assert.NoError(t, err)
	assert.Contains(t, content, "你好")
}

func TestConvertGbkToUtf8WithDifferentOutputFile(t *testing.T) {
	gbkFile, err := os.CreateTemp("", "testfile*.txt")
	assert.NoError(t, err)
	defer os.Remove(gbkFile.Name())

	utf8File, err := os.CreateTemp("", "utf8file*.txt")
	assert.NoError(t, err)
	defer os.Remove(utf8File.Name())

	// Write Chinese "你好" in GBK encoding
	err = WriteGBKFile(gbkFile.Name(), "你好")
	assert.NoError(t, err)
	RemoveIfExists(utf8File.Name(), t)

	// Convert (simulate Convert.main([gbkFile, utf8File]))
	err = ConvertFileGbkToUtf8Out(gbkFile.Name(), utf8File.Name())
	assert.NoError(t, err)

	// utf8File should exist, and contain "你好"
	_, err = os.Stat(utf8File.Name())
	assert.NoError(t, err)

	content, err := ReadUTF8File(utf8File.Name())
	assert.NoError(t, err)
	assert.Contains(t, content, "你好")
}

func TestIOExceptionIsHandled(t *testing.T) {
	// Use a non-existent file (simulate Convert.main([nonexistent file]))
	nonExistent := "/not/exists/input/file.txt"
	err := ConvertFileInPlaceGbkToUtf8(nonExistent)
	assert.Error(t, err)
}