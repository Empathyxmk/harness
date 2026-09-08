package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
	"google_mail_importer/tests"
)

func TestIoProvider_GetSuccess(t *testing.T) {
	provider := &tests.DummyIoProvider[string]{Throw: false, Value: "success"}
	provider.On("Get").Return("success", nil)
	val, err := provider.Get()
	require.NoError(t, err)
	assert.Equal(t, "success", val)
}

func TestIoProvider_GetThrowsError(t *testing.T) {
	provider := &tests.DummyIoProvider[string]{Throw: true}
	provider.On("Get").Return("", tests.TestError)
	_, err := provider.Get()
	assert.Error(t, err)
}