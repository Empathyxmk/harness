package public_tests

import (
	"strings"
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

func TestOutputPublic_EnumFormat(t *testing.T) {
	assert.True(t, strings.EqualFold(PNG.GetFormat(), "png"))
	assert.True(t, strings.ToUpper(JPG.GetFormat()) == "JPG")
}