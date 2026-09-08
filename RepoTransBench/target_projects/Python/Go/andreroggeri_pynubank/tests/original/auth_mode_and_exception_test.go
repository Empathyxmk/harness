package original

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

// Simulate enum as type (Go doesn't natively support Python-like enums)
type AuthMode int

const (
	UNAUTHENTICATED AuthMode = iota
	WEB
	APP
)

type NuException struct {
	msg string
}

func (e *NuException) Error() string {
	return e.msg
}

type NuInvalidAuthenticationMethod struct {
	NuException
}

type NuMissingCreditCard struct {
	NuException
}

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

// =============== Tests ===================

func TestAuthModeEnum(t *testing.T) {
	assert.Equal(t, int(UNAUTHENTICATED), 0)
	assert.Equal(t, int(WEB), 1)
	assert.Equal(t, int(APP), 2)
}

type dummyR struct {
	_auth_mode AuthMode
}

func (d *dummyR) GetAuthMode() AuthMode { return d._auth_mode }

func (d *dummyR) fooAllowed() (string, error) {
	return "allowed", nil
}
func (d *dummyR) fooDenied() (string, error) {
	return "denied", nil
}

func TestRequiresAuthModeSuccess(t *testing.T) {
	d := &dummyR{_auth_mode: WEB}
	secured := requiresAuthMode(WEB)(func(self interface{}) (string, error) {
		return self.(*dummyR).fooAllowed()
	})
	out, err := secured(d)
	require.NoError(t, err)
	assert.Equal(t, "allowed", out)
}

func TestRequiresAuthModeFailure(t *testing.T) {
	d := &dummyR{_auth_mode: UNAUTHENTICATED}
	secured := requiresAuthMode(WEB)(func(self interface{}) (string, error) {
		return self.(*dummyR).fooDenied()
	})
	_, err := secured(d)
	assert.Error(t, err)
	_, ok := err.(*NuInvalidAuthenticationMethod)
	assert.True(t, ok)
}

func TestNuExceptionMessage(t *testing.T) {
	e := &NuException{"hello"}
	assert.Equal(t, "hello", e.Error())
}

func TestNuInvalidAuthException(t *testing.T) {
	msg := "Bad auth"
	exc := &NuInvalidAuthenticationMethod{NuException{msg}}
	assert.True(t, exc != nil)
	assert.Contains(t, exc.Error(), msg)
}

func TestNuMissingCreditCardException(t *testing.T) {
	e := &NuMissingCreditCard{NuException{"missing credit card"}}
	assert.Contains(t, e.Error(), "missing credit card")
}

type fakeResp struct {
	statusCode int
	url        string
}

func fakeResponse() *fakeResp {
	return &fakeResp{statusCode: 404, url: "http://test"}
}

func TestRequestException(t *testing.T) {
	r := fakeResponse()
	exc := &NuRequestException{statusCode: r.statusCode, url: r.url}
	assert.Equal(t, 404, exc.statusCode)
	assert.Equal(t, "http://test", exc.url)
	assert.Contains(t, exc.Error(), "The request made failed with HTTP status code")
}