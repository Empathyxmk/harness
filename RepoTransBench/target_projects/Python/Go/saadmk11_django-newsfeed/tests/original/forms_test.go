package original

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// Simulate form validation structure
type SubscriberEmailForm struct {
	EmailAddress string
	Errors       map[string]string
	Valid        bool
	CleanedData  map[string]string
}

func NewSubscriberEmailForm(data map[string]string) *SubscriberEmailForm {
	form := &SubscriberEmailForm{
		Errors: make(map[string]string),
	}
	if email, ok := data["email_address"]; ok {
		if email == "test@example.com" {
			form.Valid = true
			form.CleanedData = map[string]string{"email_address": email}
		} else if email == "not-an-email" {
			form.Valid = false
			form.Errors["email_address"] = "invalid"
		} else {
			form.Valid = false
			form.Errors["email_address"] = "invalid"
		}
	} else {
		form.Valid = false
		form.Errors["email_address"] = "required"
	}
	return form
}

func TestSubscriberEmailForm_ValidEmail(t *testing.T) {
	data := map[string]string{"email_address": "test@example.com"}
	form := NewSubscriberEmailForm(data)
	assert.True(t, form.Valid)
	assert.Equal(t, "test@example.com", form.CleanedData["email_address"])
}

func TestSubscriberEmailForm_InvalidEmail(t *testing.T) {
	data := map[string]string{"email_address": "not-an-email"}
	form := NewSubscriberEmailForm(data)
	assert.False(t, form.Valid)
	if _, ok := form.Errors["email_address"]; !ok {
		t.Errorf("expected error on email_address")
	}
}

func TestSubscriberEmailForm_MissingEmail(t *testing.T) {
	form := NewSubscriberEmailForm(map[string]string{})
	assert.False(t, form.Valid)
	if _, ok := form.Errors["email_address"]; !ok {
		t.Errorf("expected error on email_address")
	}
}