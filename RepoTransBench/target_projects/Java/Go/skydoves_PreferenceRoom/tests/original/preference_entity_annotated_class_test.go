package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PreferenceEntityAnnotatedClass struct {
	entityName      string
	isDefault       bool
	isEncryption    bool
	encryptionKey   string
}

func NewPreferenceEntityAnnotatedClass(entityName string, hasDefault, hasEncryption bool, encryptionVal string) (PreferenceEntityAnnotatedClass, error) {
	if entityName == "" {
		return PreferenceEntityAnnotatedClass{}, errors.New("missing entity name")
	}
	return PreferenceEntityAnnotatedClass{entityName, hasDefault, hasEncryption, encryptionVal}, nil
}

func TestMissingEntityNameThrows(t *testing.T) {
	_, err := NewPreferenceEntityAnnotatedClass("", false, false, "")
	assert.Error(t, err)
}

func TestWithDefaultPreferenceAndEncryptEntity(t *testing.T) {
	entityName := "EntityX"
	encryptionVal := "ENCRYPTED_VALUE"
	clz, err := NewPreferenceEntityAnnotatedClass(entityName, true, true, encryptionVal)
	assert.NoError(t, err)
	assert.Equal(t, "EntityX", clz.entityName)
	assert.True(t, clz.isDefault)
	assert.True(t, clz.isEncryption)
	assert.Equal(t, "ENCRYPTED_VALUE", clz.encryptionKey)
}