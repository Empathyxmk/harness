package public_tests

import (
	"bufio"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FileCommandInputPublic struct {
	File   *os.File
	Reader *bufio.Scanner
}

func NewFileCommandInputPublic(filename string) (*FileCommandInputPublic, error) {
	f, err := os.Open(filename)
	if err != nil {
		return nil, err
	}
	return &FileCommandInputPublic{
		File:   f,
		Reader: bufio.NewScanner(f),
	}, nil
}

func (i *FileCommandInputPublic) ReadLine() (string, error) {
	if i.Reader == nil {
		return "", nil
	}
	if i.Reader.Scan() {
		return i.Reader.Text(), nil
	}
	return "", nil
}

func (i *FileCommandInputPublic) Close() error {
	return i.File.Close()
}

func TestReadLinesFromFile(t *testing.T) {
	tempFile, err := os.CreateTemp("", "publictestinput*.tmp")
	assert.NoError(t, err)
	defer os.Remove(tempFile.Name())
	_, err = tempFile.WriteString("Alpha\nBeta\nGamma\n")
	assert.NoError(t, err)
	tempFile.Close()

	input, err := NewFileCommandInputPublic(tempFile.Name())
	assert.NoError(t, err)
	defer input.Close()

	line, _ := input.ReadLine()
	assert.Equal(t, "Alpha", line)
	line, _ = input.ReadLine()
	assert.Equal(t, "Beta", line)
	line, _ = input.ReadLine()
	assert.Equal(t, "Gamma", line)
	line, _ = input.ReadLine()
	assert.True(t, line == "" || line == "\x00")
}