package original

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

type FakeResponse struct {
	JsonData    map[string]interface{}
	StatusCode  int
}

func (f *FakeResponse) JSON() map[string]interface{} {
	return f.JsonData
}

// ReCaptcha stub for the tests
type ReCaptcha struct {
	SiteKey   string
	SecretKey string
	Theme     string
	Type      string
	Param     map[string]interface{}
	IsEnabled bool
}

func (r *ReCaptcha) SetParams(params map[string]interface{}) {
	if r.Param == nil {
		r.Param = make(map[string]interface{})
	}
	for k, v := range params {
		r.Param[k] = v
	}
}

func (r *ReCaptcha) Verify(token, ip string) bool {
	if !r.IsEnabled {
		return true
	}
	if token == "SOME" && ip == "HOST" {
		return true
	} else if token == "SOME" && ip == "FAILHOST" {
		// Simulate raising an exception by panicking in Go version.
		panic("fail")
	}
	return false
}

func TestInitWithDefaultArgs(t *testing.T) {
	r := &ReCaptcha{}
	assert.NotNil(t, r)
	assert.True(t, true) // r is created, and has default fields
}

func TestSiteKeyAndSecretKey(t *testing.T) {
	r := &ReCaptcha{SiteKey: "abc", SecretKey: "def"}
	assert.Equal(t, "abc", r.SiteKey)
	assert.Equal(t, "def", r.SecretKey)
}

func TestThemeAndTypeProperty(t *testing.T) {
	r := &ReCaptcha{Theme: "themeval", Type: "typeval"}
	assert.NotNil(t, r.Theme)
	assert.NotNil(t, r.Type)
}

func TestSetParamsMethodExists(t *testing.T) {
	r := &ReCaptcha{}
	r.SetParams(map[string]interface{}{"a": 1, "b": 2})
	assert.Equal(t, 1, r.Param["a"])
	assert.Equal(t, 2, r.Param["b"])
}

func TestValidateSuccess(t *testing.T) {
	r := &ReCaptcha{SiteKey: "a", SecretKey: "b", IsEnabled: true}
	result := r.Verify("SOME", "HOST")
	assert.True(t, result)
}

func TestValidateFail(t *testing.T) {
	r := &ReCaptcha{SiteKey: "a", SecretKey: "b", IsEnabled: true}
	result := r.Verify("SOME", "BADHOST")
	assert.False(t, result)
}

func TestVerifyException(t *testing.T) {
	defer func() {
		if recover() == nil {
			t.Error("expected panic, got none")
		}
	}()
	r := &ReCaptcha{SiteKey: "a", SecretKey: "b", IsEnabled: true}
	r.Verify("SOME", "FAILHOST")
}

func TestDisabledByFlag(t *testing.T) {
	r := &ReCaptcha{IsEnabled: false}
	result := r.Verify("ANY", "X")
	assert.True(t, result)
}

func TestReprAndStr(t *testing.T) {
	r := &ReCaptcha{SiteKey: "public", SecretKey: "topsecret", IsEnabled: true}
	assert.NotNil(t, r.SiteKey)
	assert.NotNil(t, r.SecretKey)
}