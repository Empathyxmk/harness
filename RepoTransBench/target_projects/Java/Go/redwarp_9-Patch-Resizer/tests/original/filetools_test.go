package original

import (
	"bufio"
	"errors"
	"os"
	"path/filepath"
	"testing"

	"github.com/stretchr/testify/assert"
)

// Mock FileTools implementation for copying files
func CopyFile(src, dst string) error {
	if src == "" || dst == "" {
		return errors.New("missing file path")
	}
	srcInfo, err := os.Stat(src)
	if err != nil {
		// Java version invokes System.exit, we'll return an error for Go
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
		// Output file can't be written (maybe folder), simulate IOException by returning error
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

func TestFileTools_CopyFileNormal(t *testing.T) {
	tempInput, err := os.CreateTemp("", "input*.txt")
	assert.NoError(t, err)
	defer os.Remove(tempInput.Name())
	tempOutput, err := os.CreateTemp("", "output*.txt")
	assert.NoError(t, err)
	tempOutput.Close()
	os.Remove(tempOutput.Name())

	_, err = tempInput.WriteString("Hello World!")
	assert.NoError(t, err)
	tempInput.Close()

	err = CopyFile(tempInput.Name(), tempOutput.Name())
	assert.NoError(t, err, "CopyFile should not error on normal copy")

	// file should exist and content should match
	content := ""
	file, err := os.Open(tempOutput.Name())
	assert.NoError(t, err)
	scanner := bufio.NewScanner(file)
	if scanner.Scan() {
		content = scanner.Text()
	}
	file.Close()
	assert.Equal(t, "Hello World!", content, "Copied content should match")
	os.Remove(tempOutput.Name())
}

func TestFileTools_CopyFileInputFileNotExist(t *testing.T) {
	tempOutput, err := os.CreateTemp("", "output*.txt")
	assert.NoError(t, err)
	tempOutput.Close()
	os.Remove(tempOutput.Name())

	err = CopyFile("not_exist_file.xyz", tempOutput.Name())
	assert.Error(t, err, "Expected error if input file does not exist")
}

func TestFileTools_CopyFileIOException(t *testing.T) {
	tempInput, err := os.CreateTemp("", "input*.txt")
	assert.NoError(t, err)
	defer os.Remove(tempInput.Name())

	_, err = tempInput.WriteString("Hello World!")
	assert.NoError(t, err)
	tempInput.Close()

	folder, err := os.MkdirTemp("", "somedummy")
	assert.NoError(t, err)
	defer os.RemoveAll(folder)

	err = CopyFile(tempInput.Name(), folder)
	assert.Error(t, err, "Should error when output is a directory")
}