package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestSharedPreferencesSmsStoragePublic_PutAndGetValue(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	storage.ClearPreferences()
	storage.PutString("animal", "dog")
	assert.Equal(t, "dog", storage.GetString("animal", ""))
}

func TestSharedPreferencesSmsStoragePublic_OverwriteValue(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	storage.PutString("language", "Python")
	storage.PutString("language", "Go")
	assert.Equal(t, "Go", storage.GetString("language", ""))
}

func TestSharedPreferencesSmsStoragePublic_GetDefaultIfNotPresent(t *testing.T) {
	storage := NewSharedPreferencesSmsStorage()
	assert.Equal(t, "default", storage.GetString("missing-key", "default"))
}