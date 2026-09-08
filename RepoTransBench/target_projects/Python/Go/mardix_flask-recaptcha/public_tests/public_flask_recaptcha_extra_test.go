package public_tests

import (
	"strings"
	"testing"
	"github.com/stretchr/testify/assert"
)

// Mimics a ReCaptcha struct & get_code method for simple HTML/test logic.
type ReCaptcha struct {
	SiteKey string
	Theme   string
}

func (r *ReCaptcha) GetCode() string {
	code := "<div class='g-recaptcha' data-sitekey='" + r.SiteKey + "'"
	if r.Theme != "" {
		code += " data-theme=\"" + r.Theme + "\""
	}
	code += "></div>"
	return code
}

func TestPublicHtmlGenerationDifferent(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.SiteKey = "pub-key-test"
	html := recaptcha.GetCode()
	assert.Contains(t, html, "pub-key-test")
	assert.Contains(t, html, "g-recaptcha")
}

func TestPublicThemeInHtml(t *testing.T) {
	recaptcha := &ReCaptcha{}
	recaptcha.SiteKey = "test-key"
	recaptcha.Theme = "dark"
	html := recaptcha.GetCode()
	assert.Contains(t, html, "data-theme=\"dark\"")
}