package public_tests

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

// Note: In Go, we can't directly test DEFAULTS.get or dictionary. Instead, we'll simulate checking a struct/map.

type Defaults struct {
	SslVerify bool
	Size      string
	Theme     string
}

func GetDefaults() map[string]interface{} {
	return map[string]interface{}{
		"ssl_verify": true,
		"size":       "compact",
	}
}

type ReCaptcha struct {
	SiteKey string
	SecretKey string
	Options  map[string]string
}

func NewReCaptchaWithConfig(config map[string]interface{}) *ReCaptcha {
	r := &ReCaptcha{
		Options: make(map[string]string),
	}
	if v, ok := config["RECAPTCHA_SITE_KEY"].(string); ok {
		r.SiteKey = v
	}
	if v, ok := config["RECAPTCHA_SECRET_KEY"].(string); ok {
		r.SecretKey = v
	}
	if opts, ok := config["RECAPTCHA_OPTIONS"].(map[string]string); ok {
		r.Options = opts
	}
	return r
}

func TestPublicDefaultsAreDifferent(t *testing.T) {
	defaults := GetDefaults()
	assert.Equal(t, true, defaults["ssl_verify"])
	_, ok := defaults["size"]
	assert.True(t, ok)
}

func TestPublicRecaptchaInitialConfig(t *testing.T) {
	config := map[string]interface{}{
		"RECAPTCHA_SITE_KEY":    "publicUnique123",
		"RECAPTCHA_SECRET_KEY":  "publicSecretABC",
		"RECAPTCHA_OPTIONS": map[string]string{
			"theme": "light",
			"size":  "compact",
		},
	}
	recaptcha := NewReCaptchaWithConfig(config)
	assert.Equal(t, "publicUnique123", recaptcha.SiteKey)
	assert.Equal(t, "publicSecretABC", recaptcha.SecretKey)
	expectedOpts := map[string]string{
		"theme": "light",
		"size":  "compact",
	}
	assert.Equal(t, expectedOpts, recaptcha.Options)
}