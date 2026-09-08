package public_tests

import (
	"bytes"
	"io"
	"testing"

	"github.com/stretchr/testify/assert"
	"google_mail_importer/tests"
)

func TestIoProvider_ReadAllReturnsStream(t *testing.T) {
	testString := "PublicTestContent123"
	b := []byte(testString)
	reader := bytes.NewReader(b)
	data, err := tests.ReadAll(reader)
	assert.NoError(t, err)
	assert.Equal(t, testString, string(data))
}