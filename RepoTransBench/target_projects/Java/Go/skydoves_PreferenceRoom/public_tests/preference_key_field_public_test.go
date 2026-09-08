package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PreferenceKeyField struct {
	keyName        string
	typeStringName string
	className      string
}

func NewPreferenceKeyField(fieldName, typeString, keyName string, modifiers []string) (PreferenceKeyField, error) {
	isFinal := false
	isPrivate := false
	for _, m := range modifiers {
		if m == "FINAL" {
			isFinal = true
		}
		if m == "PRIVATE" {
			isPrivate = true
		}
	}
	if isPrivate {
		return PreferenceKeyField{}, errors.New("field is private")
	}
	if !isFinal {
		return PreferenceKeyField{}, errors.New("field is not final")
	}
	return PreferenceKeyField{keyName, typeString, fieldName}, nil
}

func TestDifferentBooleanField(t *testing.T) {
	field, err := NewPreferenceKeyField("isActive", "Boolean", "IsActive", []string{"FINAL"})
	assert.NoError(t, err)
	assert.Equal(t, "Boolean", field.typeStringName)
	assert.Equal(t, "IsActive", field.keyName)
	assert.Equal(t, "isActive", field.className)
}

func TestStringFieldWithAnotherCustomKeyName(t *testing.T) {
	field, err := NewPreferenceKeyField("displayName", "String", "anotherCustomKey", []string{"FINAL"})
	assert.NoError(t, err)
	assert.Equal(t, "anotherCustomKey", field.keyName)
	assert.Equal(t, "String", field.typeStringName)
}

func TestPrivateFieldThrowsPublic(t *testing.T) {
	_, err := NewPreferenceKeyField("isActive", "Boolean", "IsActive", []string{"PRIVATE"})
	assert.Error(t, err)
}

func TestNonFinalFieldThrowsPublic(t *testing.T) {
	_, err := NewPreferenceKeyField("isActive", "Boolean", "IsActive", []string{})
	assert.Error(t, err)
}