package tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PyiCloudException struct {
	msg string
}
func (e *PyiCloudException) Error() string { return e.msg }

type PyiCloudAPIResponseException struct {
	reason string
	code   *string
	retry  bool
}
func (e *PyiCloudAPIResponseException) Error() string {
	msg := e.reason
	if e.code != nil {
		msg += " (" + *e.code + ")"
	}
	if e.retry {
		msg += " Retrying"
	}
	return msg
}
type PyiCloudServiceNotActivatedException struct{ msg string }
func (e *PyiCloudServiceNotActivatedException) Error() string { return e.msg }

type PyiCloudFailedLoginException struct{ msg string }
func (e *PyiCloudFailedLoginException) Error() string { return e.msg }

type PyiCloud2SARequiredException struct{ email string }
func (e *PyiCloud2SARequiredException) Error() string {
	return "Two-step authentication required for account: " + e.email
}

type PyiCloudNoStoredPasswordAvailableException struct{ msg string }
func (e *PyiCloudNoStoredPasswordAvailableException) Error() string { return e.msg }

type PyiCloudNoDevicesException struct{ msg string }
func (e *PyiCloudNoDevicesException) Error() string { return e.msg }

func TestPyiCloudException(t *testing.T) {
	ex := &PyiCloudException{"test"}
	assert.True(t, errors.Is(ex, ex))
	assert.Equal(t, "test", ex.Error())
}

func TestPyiCloudAPIResponseExceptionBasic(t *testing.T) {
	ex := &PyiCloudAPIResponseException{reason: "error reason"}
	assert.Contains(t, ex.Error(), "error reason")
	assert.Equal(t, "error reason", ex.reason)
	assert.Nil(t, ex.code)
}

func TestPyiCloudAPIResponseExceptionFull(t *testing.T) {
	code := "42"
	ex := &PyiCloudAPIResponseException{reason: "fail", code: &code, retry: true}
	msg := ex.Error()
	assert.Contains(t, msg, "fail")
	assert.Contains(t, msg, "42")
	assert.Contains(t, msg, "Retrying")
	assert.Equal(t, "fail", ex.reason)
	assert.Equal(t, &code, ex.code)
}

func TestServiceNotActivatedException(t *testing.T) {
	ex := &PyiCloudServiceNotActivatedException{"reason"}
	assert.Contains(t, ex.Error(), "reason")
}

func TestFailedLoginException(t *testing.T) {
	ex := &PyiCloudFailedLoginException{"login fail"}
	assert.Contains(t, ex.Error(), "login fail")
}

func Test2SARequiredException(t *testing.T) {
	ex := &PyiCloud2SARequiredException{"email@email.com"}
	assert.Contains(t, ex.Error(), "Two-step authentication required for account: email@email.com")
}

func TestNoStoredPasswordException(t *testing.T) {
	ex := &PyiCloudNoStoredPasswordAvailableException{"no password"}
	assert.Contains(t, ex.Error(), "no password")
}

func TestNoDevicesException(t *testing.T) {
	ex := &PyiCloudNoDevicesException{"no device"}
	assert.Contains(t, ex.Error(), "no device")
}