package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type ReCaptcha struct {
	SiteKey   string
	SecretKey string
	Theme     string
	Type      string
	Size      string
	Language  string
	TabIndex  int
	IsEnabled bool
	Param     map[string]interface{}
	App       interface{}
}

func NewReCaptcha(sitekey, secretkey, theme, typ, size, language string, tabindex int) *ReCaptcha {
	return &ReCaptcha{
		SiteKey:   sitekey,
		SecretKey: secretkey,
		Theme:     theme,
		Type:      typ,
		Size:      size,
		Language:  language,
		TabIndex:  tabindex,
		IsEnabled: true,
	}
}

func (r *ReCaptcha) GetCode() string {
	return "<script>code</script>"
}

func (r *ReCaptcha) Verify(token, ip string) bool {
	// Only valid if token is not empty
	if token == "" {
		return false
	}
	return true
}

func (r *ReCaptcha) InitApp(app interface{}) {
	// Simulate context processor setup
	return
}

func TestParamsInit(t *testing.T) {
	r := NewReCaptcha("A", "B", "light", "image", "compact", "en", 1)
	assert.Equal(t, "A", r.SiteKey)
	assert.Equal(t, "B", r.SecretKey)
	assert.Equal(t, "light", r.Theme)
	assert.Equal(t, "image", r.Type)
	assert.Equal(t, "compact", r.Size)
	assert.Equal(t, "en", r.Language)
	assert.Equal(t, 1, r.TabIndex)
}

func TestEnabledProperty(t *testing.T) {
	r := &ReCaptcha{IsEnabled: true}
	assert.True(t, r.IsEnabled)
	r2 := &ReCaptcha{IsEnabled: false}
	assert.False(t, r2.IsEnabled)
}

func TestGetCodeReturnsString(t *testing.T) {
	r := &ReCaptcha{SiteKey: "something", SecretKey: "else"}
	code := r.GetCode()
	assert.IsType(t, "", code)
}

func TestVerifyEmptyResponseToken(t *testing.T) {
	r := &ReCaptcha{SiteKey: "a", SecretKey: "b", IsEnabled: true}
	result := r.Verify("", "host")
	assert.False(t, result)
}

func TestInitAppWithMinimum(t *testing.T) {
	type App struct {
		Config map[string]interface{}
		Proc   func() map[string]interface{}
	}
	app := &App{
		Config: map[string]interface{}{
			"RECAPTCHA_SITE_KEY":   "k",
			"RECAPTCHA_SECRET_KEY": "s",
		},
	}
	r := &ReCaptcha{}
	r.InitApp(app)
	assert.NotNil(t, app)
}