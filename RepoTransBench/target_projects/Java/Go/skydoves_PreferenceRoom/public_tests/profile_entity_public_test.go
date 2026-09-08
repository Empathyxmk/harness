package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type Profile struct {
	Name  string
	Email string
	Phone string
}

func NewProfile(name, email string) *Profile {
	return &Profile{Name: name, Email: email}
}

func (p *Profile) SetPhone(ph string) {
	p.Phone = ph
}

func TestNamePublic(t *testing.T) {
	profile := NewProfile("public_name", "public@email.org")
	profile.SetPhone("123987456")
	assert.Equal(t, "public_name", profile.Name)
}

func TestEmailPublic(t *testing.T) {
	profile := NewProfile("public_name", "public@email.org")
	profile.SetPhone("123987456")
	assert.Equal(t, "public@email.org", profile.Email)
}

func TestPhonePublic(t *testing.T) {
	profile := NewProfile("public_name", "public@email.org")
	profile.SetPhone("123987456")
	assert.Equal(t, "123987456", profile.Phone)
}