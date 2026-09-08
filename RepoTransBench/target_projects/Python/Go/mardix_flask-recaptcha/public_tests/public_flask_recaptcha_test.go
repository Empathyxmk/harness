package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type ReCaptcha struct {
	SiteKey   string
	SecretKey string
	Language  string
	Theme     string
}

func TestPublicSetAndGetSiteKey(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.SiteKey = "different_public_key"
	assert.Equal(t, "different_public_key", recaptcha.SiteKey)
}

func TestPublicSetAndGetSecretKey(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.SecretKey = "different_public_secret"
	assert.Equal(t, "different_public_secret", recaptcha.SecretKey)
}

func TestPublicLanguageSetterAndGetter(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.Language = "fr"
	assert.Equal(t, "fr", recaptcha.Language)
}

func TestPublicThemeSetterAndGetter(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.Theme = "dark"
	assert.Equal(t, "dark", recaptcha.Theme)
}