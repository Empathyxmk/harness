package public_tests

import (
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
	"netease_arrow/tests"
)

// Simulates ConvertPublicTest with different test string ("世界": "world")
func TestConvertGbkToUtf8InPlace(t *testing.T) {
	gbkFile, err := os.CreateTemp("", "public_testfile*.txt")
	assert.NoError(t, err)
	defer os.Remove(gbkFile.Name())

	utf8File, err := os.CreateTemp("", "public_utf8file*.txt")
	assert.NoError(t, err)
	defer os.Remove(utf8File.Name())

	// Write Chinese "世界" in GBK encoding
	err = tests.WriteGBKFile(gbkFile.Name(), "世界")
	assert.NoError(t, err)
	tests.RemoveIfExists(utf8File.Name(), t)

	// Simulate Convert.main([gbkFile])
	err = tests.ConvertFileInPlaceGbkToUtf8(gbkFile.Name())
	assert.NoError(t, err)
	content, err := tests.ReadUTF8File(gbkFile.Name())
	assert.NoError(t, err)
	assert.Contains(t, content, "世界")
}

func TestConvertGbkToUtf8WithDifferentOutputFile(t *testing.T) {
	gbkFile, err := os.CreateTemp("", "public_testfile*.txt")
	assert.NoError(t, err)
	defer os.Remove(gbkFile.Name())

	utf8File, err := os.CreateTemp("", "public_utf8file*.txt")
	assert.NoError(t, err)
	defer os.Remove(utf8File.Name())

	// Write Chinese "世界" in GBK encoding
	err = tests.WriteGBKFile(gbkFile.Name(), "世界")
	assert.NoError(t, err)
	tests.RemoveIfExists(utf8File.Name(), t)

	// Convert (simulate Convert.main([gbkFile, utf8File]))
	err = tests.ConvertFileGbkToUtf8Out(gbkFile.Name(), utf8File.Name())
	assert.NoError(t, err)

	// utf8File should exist and contain "世界"
	_, err = os.Stat(utf8File.Name())
	assert.NoError(t, err)

	content, err := tests.ReadUTF8File(utf8File.Name())
	assert.NoError(t, err)
	assert.Contains(t, content, "世界")
}

func TestIOExceptionIsHandled(t *testing.T) {
	nonExistent := "/definitely/doesnotexist/inputfile_public.txt"
	err := tests.ConvertFileInPlaceGbkToUtf8(nonExistent)
	assert.Error(t, err)
}