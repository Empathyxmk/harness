package public_tests

import (
	"bufio"
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
)

type InputStreamCommandInputPublic struct {
	Reader *bufio.Scanner
}

func NewInputStreamCommandInputPublic(data []byte) *InputStreamCommandInputPublic {
	return &InputStreamCommandInputPublic{
		Reader: bufio.NewScanner(bytes.NewReader(data)),
	}
}

func (i *InputStreamCommandInputPublic) ReadLine() string {
	if i.Reader.Scan() {
		return i.Reader.Text()
	}
	return ""
}

func TestReadLineFromInputStream(t *testing.T) {
	data := []byte("Delta\nEpsilon\n")
	input := NewInputStreamCommandInputPublic(data)

	assert.Equal(t, "Delta", input.ReadLine())
	assert.Equal(t, "Epsilon", input.ReadLine())
	line := input.ReadLine()
	assert.Equal(t, "", line)
}