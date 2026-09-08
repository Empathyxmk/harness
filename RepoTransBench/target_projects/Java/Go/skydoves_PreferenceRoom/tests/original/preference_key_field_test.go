package original

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

func TestBooleanField(t *testing.T) {
	field, err := NewPreferenceKeyField("flag", "Boolean", "Flag", []string{"FINAL"})
	assert.NoError(t, err)
	assert.Equal(t, "Boolean", field.typeStringName)
	assert.Equal(t, "Flag", field.keyName)
	assert.Equal(t, "flag", field.className)
}

func TestStringFieldWithCustomKeyName(t *testing.T) {
	field, err := NewPreferenceKeyField("username", "String", "customKey", []string{"FINAL"})
	assert.NoError(t, err)
	assert.Equal(t, "customKey", field.keyName)
	assert.Equal(t, "String", field.typeStringName)
}

func TestPrivateFieldThrows(t *testing.T) {
	_, err := NewPreferenceKeyField("flag", "Boolean", "Flag", []string{"PRIVATE"})
	assert.Error(t, err)
}

func TestNonFinalFieldThrows(t *testing.T) {
	_, err := NewPreferenceKeyField("flag", "Boolean", "Flag", []string{})
	assert.Error(t, err)
}