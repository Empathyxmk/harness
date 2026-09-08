package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

// You must implement a setToken helper in Go.
type DummySession struct {
	Token map[string]interface{}
}

func setToken(sess *DummySession, token map[string]interface{}) {
	sess.Token = token
}

func TestSetTokenPublicDiffToken(t *testing.T) {
	sess := &DummySession{}
	setToken(sess, map[string]interface{}{
		"access_token": "unicorn_xyz",
		"token_type":   "Bearer",
	})
	assert.NotNil(t, sess.Token)
	assert.Equal(t, "unicorn_xyz", sess.Token["access_token"])
}

func TestSetTokenPublicOtherDiff(t *testing.T) {
	sess := &DummySession{}
	setToken(sess, map[string]interface{}{
		"access_token": "golden_public_token",
		"token_type":   "macaroons",
	})
	assert.NotNil(t, sess.Token)
	assert.Equal(t, "golden_public_token", sess.Token["access_token"])
}