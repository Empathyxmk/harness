package original

import (
	"bytes"
	"testing"

	"github.com/stretchr/testify/assert"
	"project/company"
)

func TestMainWithNoArgs(t *testing.T) {
	var buf bytes.Buffer
	company.SetOutput(&buf)
	company.MainEntry([]string{})
	company.SetOutput(nil)
	output := buf.String()
	assert.True(t, len(output) > 0, "Output should not be empty")
}

func TestMainWithNormalArg(t *testing.T) {
	var buf bytes.Buffer
	company.SetOutput(&buf)
	company.MainEntry([]string{"4567"})
	company.SetOutput(nil)
	output := buf.String()
	assert.True(t, len(output) > 0, "Output should not be empty")
}

func TestMainWithAlphaArg(t *testing.T) {
	var buf bytes.Buffer
	company.SetOutput(&buf)
	company.MainEntry([]string{"abc123"})
	company.SetOutput(nil)
	output := buf.String()
	assert.True(t, len(output) > 0, "Output should not be empty")
}

func TestMainWithEmptyArg(t *testing.T) {
	var buf bytes.Buffer
	company.SetOutput(&buf)
	company.MainEntry([]string{""})
	company.SetOutput(nil)
	output := buf.String()
	assert.True(t, len(output) > 0, "Output should not be empty")
}