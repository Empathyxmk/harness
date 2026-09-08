package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Model struct {
	Object   string
	ID       string
	Created  int
	Name     string
	OwnedBy  string
	XHeaders map[string]string
}

func TestModelInitAndFields(t *testing.T) {
	model := Model{
		Object:   "special_object",
		ID:       "test_id_2",
		Created:  1234567,
		Name:     "SuperGigaModel",
		OwnedBy:  "public_giga_owner",
		XHeaders: nil,
	}
	assert.Equal(t, "test_id_2", model.ID)
	assert.Equal(t, "special_object", model.Object)
	assert.Equal(t, "SuperGigaModel", model.Name)
	assert.Equal(t, "public_giga_owner", model.OwnedBy)
	assert.IsType(t, int(0), model.Created)
	assert.Nil(t, model.XHeaders)
}

func TestModelStrAndReprPublic(t *testing.T) {
	model := Model{
		Object:  "public_object",
		ID:      "AAA_public",
		Created: 1010101,
		Name:    "PublicModel",
		OwnedBy: "someone_else",
	}
	text := model.Name + " " + model.ID
	assert.Contains(t, text, "AAA_public")
	assert.Contains(t, text, "PublicModel")
}