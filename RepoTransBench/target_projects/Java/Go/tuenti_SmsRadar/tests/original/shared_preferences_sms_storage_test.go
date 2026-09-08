package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSharedPreferencesSmsStorage_DefaultValueIfNotEdited(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	storage.Clear()
	assert.Equal(t, -1, storage.GetLastSmsIntercepted())
}

func TestSharedPreferencesSmsStorage_UpdateLastSmsIntercepted(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	storage.Clear()
	storage.UpdateLastSmsIntercepted(1)
	assert.Equal(t, 1, storage.GetLastSmsIntercepted())
}

func TestSharedPreferencesSmsStorage_IsFirstSmsInterceptedInitiallyTrue(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	storage.Clear()
	assert.True(t, storage.IsFirstSmsIntercepted())
}