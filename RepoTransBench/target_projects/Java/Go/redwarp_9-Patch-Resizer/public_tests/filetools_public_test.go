package public_tests

import (
	"bufio"
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mock FileTools implementation for copying files for public test
func CopyFilePublic(src, dst string) error {
	if src == "" || dst == "" {
		return errors.New("missing file path")
	}
	srcInfo, err := os.Stat(src)
	if err != nil {
		return errors.New("input file does not exist")
	}
	if srcInfo.IsDir() {
		return errors.New("source cannot be a directory")
	}
	srcFile, err := os.Open(src)
	if err != nil {
		return err
	}
	defer srcFile.Close()
	dstParent := filepath.Dir(dst)
	os.MkdirAll(dstParent, 0755)

	dstFile, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer dstFile.Close()
	_, err = srcFile.Seek(0, 0)
	if err != nil {
		return err
	}

	scanner := bufio.NewScanner(srcFile)
	writer := bufio.NewWriter(dstFile)
	for scanner.Scan() {
		_, err := writer.WriteString(scanner.Text())
		if err != nil {
			return err
		}
	}
	writer.Flush()
	return scanner.Err()
}

func TestFileToolsPublic_CopyFileNormal(t *testing.T) {
	tempInput, err := os.CreateTemp("", "pinput*.dat")
	assert.NoError(t, err)
	defer os.Remove(tempInput.Name())
	tempOutput, err := os.CreateTemp("", "poutput*.dat")
	assert.NoError(t, err)
	tempOutput.Close()
	os.Remove(tempOutput.Name())

	_, err = tempInput.WriteString("Public Test Data!!")
	assert.NoError(t, err)
	tempInput.Close()

	err = CopyFilePublic(tempInput.Name(), tempOutput.Name())
	assert.NoError(t, err, "CopyFilePublic should not error on normal copy")

	content := ""
	file, err := os.Open(tempOutput.Name())
	assert.NoError(t, err)
	scanner := bufio.NewScanner(file)
	if scanner.Scan() {
		content = scanner.Text()
	}
	file.Close()
	assert.Equal(t, "Public Test Data!!", content, "Copied content should match")
	os.Remove(tempOutput.Name())
}

func TestFileToolsPublic_CopyFileInputFileNotExist(t *testing.T) {
	tempOutput, err := os.CreateTemp("", "poutput*.dat")
	assert.NoError(t, err)
	tempOutput.Close()
	os.Remove(tempOutput.Name())

	err = CopyFilePublic("missing_file_abc123.txt", tempOutput.Name())
	assert.Error(t, err, "Expected error if input file does not exist")
}

func TestFileToolsPublic_CopyFileIOException(t *testing.T) {
	tempInput, err := os.CreateTemp("", "pinput*.dat")
	assert.NoError(t, err)
	defer os.Remove(tempInput.Name())

	_, err = tempInput.WriteString("Public Test Data!!")
	assert.NoError(t, err)
	tempInput.Close()

	folder, err := os.MkdirTemp("", "pfolder")
	assert.NoError(t, err)
	defer os.RemoveAll(folder)

	err = CopyFilePublic(tempInput.Name(), folder)
	assert.Error(t, err, "Should error when output is a directory")
}