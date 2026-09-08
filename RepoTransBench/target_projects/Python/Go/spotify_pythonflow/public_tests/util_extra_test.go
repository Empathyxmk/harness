package public_tests

import (
	"testing"
	"strings"

	"github.com/stretchr/testify/assert"
)

func Uppercase(s string) string {
	return strings.ToUpper(s)
}

func TestUppercasePublic(t *testing.T) {
	assert.Equal(t, "XYZ", Uppercase("xyz"))
	assert.Equal(t, "", Uppercase(""))
}