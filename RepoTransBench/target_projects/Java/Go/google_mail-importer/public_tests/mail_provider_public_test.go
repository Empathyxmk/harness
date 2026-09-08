package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"google_mail_importer/tests"
)

type AnotherDummyMailProvider struct {
	ShouldThrow bool
}

func (d *AnotherDummyMailProvider) Get() (int, error) {
	if d.ShouldThrow {
		return 0, tests.TestError
	}
	return 12345, nil
}

func TestMailProvider_PublicGetSuccess(t *testing.T) {
	provider := &AnotherDummyMailProvider{ShouldThrow: false}
	val, err := provider.Get()
	require.NoError(t, err)
	assert.Equal(t, 12345, val)
}

func TestMailProvider_PublicGetThrowsError(t *testing.T) {
	provider := &AnotherDummyMailProvider{ShouldThrow: true}
	_, err := provider.Get()
	assert.Error(t, err)
}