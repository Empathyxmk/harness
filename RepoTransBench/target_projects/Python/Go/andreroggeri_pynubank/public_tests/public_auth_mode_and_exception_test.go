package public_tests

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

type AuthMode int

const (
	UNAUTHENTICATED AuthMode = iota
	WEB
	APP
)

type NuException struct{ msg string }

func (e *NuException) Error() string { return e.msg }

type NuInvalidAuthenticationMethod struct{ NuException }
type NuMissingCreditCard struct{ NuException }
type NuRequestException struct {
	statusCode int
	url        string
}

func (e *NuRequestException) Error() string {
	return fmt.Sprintf("The request made failed with HTTP status code %d at %s", e.statusCode, e.url)
}

func requiresAuthMode(required AuthMode) func(fn func(self interface{}) (string, error)) func(self interface{}) (string, error) {
	return func(fn func(self interface{}) (string, error)) func(self interface{}) (string, error) {
		return func(self interface{}) (string, error) {
			t, ok := self.(interface{ GetAuthMode() AuthMode })
			if !ok {
				return "", &NuInvalidAuthenticationMethod{NuException{"No auth mode"}}
			}
			if t.GetAuthMode() != required {
				return "", &NuInvalidAuthenticationMethod{NuException{"Wrong auth mode"}}
			}
			return fn(self)
		}
	}
}

type dummyPublic struct {
	_auth_mode AuthMode
}

func (d *dummyPublic) GetAuthMode() AuthMode { return d._auth_mode }

func (d *dummyPublic) barGranted() (string, error) {
	return "granted", nil
}
func (d *dummyPublic) barRefused() (string, error) {
	return "refused", nil
}

func TestAuthModeEnumPublic(t *testing.T) {
	assert.Equal(t, 0, int(UNAUTHENTICATED))
	assert.NotEqual(t, 0, int(WEB))
	assert.NotEqual(t, WEB, APP)
}

func TestRequiresAuthModeSuccessPublic(t *testing.T) {
	d := &dummyPublic{_auth_mode: APP}
	secured := requiresAuthMode(APP)(func(self interface{}) (string, error) {
		return self.(*dummyPublic).barGranted()
	})
	out, err := secured(d)
	assert.NoError(t, err)
	assert.Equal(t, "granted", out)
}

func TestRequiresAuthModeFailurePublic(t *testing.T) {
	d := &dummyPublic{_auth_mode: WEB}
	secured := requiresAuthMode(APP)(func(self interface{}) (string, error) {
		return self.(*dummyPublic).barRefused()
	})
	_, err := secured(d)
	assert.Error(t, err)
}

func TestNuExceptionMessagePublic(t *testing.T) {
	e := &NuException{"goodbye world"}
	assert.Equal(t, "goodbye world", e.Error())
}

func TestNuInvalidAuthExceptionPublic(t *testing.T) {
	msg := "Authentication failed"
	exc := &NuInvalidAuthenticationMethod{NuException{msg}}
	assert.True(t, exc != nil)
	assert.Contains(t, exc.Error(), msg)
}

func TestNuMissingCreditCardExceptionPublic(t *testing.T) {
	e := &NuMissingCreditCard{NuException{"missing credit card"}}
	assert.Contains(t, e.Error(), "credit card")
	assert.Contains(t, e.Error(), "missing")
}

type fakeRespPublic struct {
	statusCode int
	url        string
}

func fakeResponsePublic() *fakeRespPublic {
	return &fakeRespPublic{statusCode: 500, url: "http://other-url"}
}

func TestRequestExceptionPublic(t *testing.T) {
	r := fakeResponsePublic()
	exc := &NuRequestException{statusCode: r.statusCode, url: r.url}
	assert.Equal(t, 500, exc.statusCode)
	assert.Equal(t, "http://other-url", exc.url)
	assert.Contains(t, exc.Error(), "The request made failed with HTTP status code")
}