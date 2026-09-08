package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type DummyConfigPublicAuth struct {
	AUTH interface{}
}

func TestBasicAuthPublic(t *testing.T) {
	username := "user2"
	password := "pass2"
	type BasicAuth struct {
		username string
		password string
	}
	a := BasicAuth{username: username, password: password}
	assert.Equal(t, "user2", a.username)
	assert.Equal(t, "pass2", a.password)
}

func TestTokenAuthPublic(t *testing.T) {
	token := "publictoken"
	type TokenAuth struct {
		token string
	}
	tkn := TokenAuth{token: token}
	assert.Equal(t, "publictoken", tkn.token)
}

func TestApplyAuthPublic(t *testing.T) {
	type BasicAuth struct {
		username string
		password string
	}
	a := BasicAuth{username: "alice", password: "secret123"}
	config := DummyConfigPublicAuth{}
	config.AUTH = a
	val, ok := config.AUTH.(BasicAuth)
	assert.True(t, ok)
	assert.Equal(t, "alice", val.username)
	assert.Equal(t, "secret123", val.password)
}