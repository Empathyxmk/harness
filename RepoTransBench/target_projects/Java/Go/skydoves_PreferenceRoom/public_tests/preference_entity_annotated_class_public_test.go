package public_tests

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

func TestMissingEntityNameThrowsPublic(t *testing.T) {
	_, err := NewPreferenceEntityAnnotatedClass("", false, false, "")
	assert.Error(t, err)
}

func TestWithDifferentDefaultPreferenceAndEncryptEntity(t *testing.T) {
	entityName := "EntityY"
	encryptionVal := "PUBLIC_ENCRYPTED_VAL"
	clz, err := NewPreferenceEntityAnnotatedClass(entityName, true, true, encryptionVal)
	assert.NoError(t, err)
	assert.Equal(t, "EntityY", clz.entityName)
	assert.True(t, clz.isDefault)
	assert.True(t, clz.isEncryption)
	assert.Equal(t, "PUBLIC_ENCRYPTED_VAL", clz.encryptionKey)
}