package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Profile struct {
	Name  string
	Email string
}

func NewProfile(name, email string) *Profile {
	return &Profile{Name: name, Email: email}
}

func TestProfileNameIsSetPublic(t *testing.T) {
	p := NewProfile("public_test_user", "public@email.com")
	assert.Equal(t, "public_test_user", p.Name)
}

func TestProfileEmailIsSetPublic(t *testing.T) {
	p := NewProfile("public_test_user", "public@email.com")
	assert.Equal(t, "public@email.com", p.Email)
}