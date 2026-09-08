package public_tests

import (
	"bufio"
	"os"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FileCommandOutputPublic struct {
	File *os.File
	Writer *bufio.Writer
}

func NewFileCommandOutputPublic(filename string) (*FileCommandOutputPublic, error) {
	f, err := os.Create(filename)
	if err != nil {
		return nil, err
	}
	return &FileCommandOutputPublic{
		File: f,
		Writer: bufio.NewWriter(f),
	}, nil
}

func (f *FileCommandOutputPublic) Print(s string) {
	f.Writer.WriteString(s)
}
func (f *FileCommandOutputPublic) Println(s string) {
	f.Writer.WriteString(s + "\n")
}
func (f *FileCommandOutputPublic) Flush() {
	f.Writer.Flush()
}
func (f *FileCommandOutputPublic) Close() {
	f.Writer.Flush()
	f.File.Close()
}

func TestWriteToFile(t *testing.T) {
	tempFile, err := os.CreateTemp("", "publictestoutput*.tmp")
	assert.NoError(t, err)
	defer os.Remove(tempFile.Name())

	output, err := NewFileCommandOutputPublic(tempFile.Name())
	assert.NoError(t, err)
	output.Print("PublicTest Output Line")
	output.Println(" 12345")
	output.Flush()
	output.Close()

	f, err := os.Open(tempFile.Name())
	assert.NoError(t, err)
	defer f.Close()
	scanner := bufio.NewScanner(f)
	content := ""
	secondLine := ""
	if scanner.Scan() {
		content = scanner.Text()
	}
	if scanner.Scan() {
		secondLine = scanner.Text()
	}
	assert.Contains(t, content, "PublicTest Output Line")
	assert.Contains(t, secondLine, "12345")
}