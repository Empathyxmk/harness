package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"google_mail_importer/tests"
)

func TestMailProvider_GetSuccess(t *testing.T) {
	provider := &tests.DummyMailProvider[string]{Throw: false, Value: "success"}
	provider.On("Get").Return("success", nil)
	val, err := provider.Get()
	require.NoError(t, err)
	assert.Equal(t, "success", val)
}

func TestMailProvider_GetThrowsError(t *testing.T) {
	provider := &tests.DummyMailProvider[string]{Throw: true}
	provider.On("Get").Return("", tests.TestError)
	_, err := provider.Get()
	assert.Error(t, err)
}