package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type OutputFormat string

const (
	PNG OutputFormat = "png"
	JPG OutputFormat = "jpg"
)

func (o OutputFormat) GetFormat() string {
	return string(o)
}

func TestOutput_EnumFormat(t *testing.T) {
	assert.Equal(t, "png", PNG.GetFormat())
	assert.Equal(t, "jpg", JPG.GetFormat())
}