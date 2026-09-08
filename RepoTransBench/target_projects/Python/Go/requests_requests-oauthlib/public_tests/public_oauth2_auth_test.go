package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

// OAuth2Stub and example
type OAuth2Stub struct {
	ClientID string
	Token    map[string]interface{}
}

func (o *OAuth2Stub) AuthHeader() string {
	if o.Token == nil {
		return ""
	}
	return "Bearer " + o.Token["access_token"].(string)
}

func TestPublicOAuth2AuthHeaderDiffData(t *testing.T) {
	clientID := "public_client_id"
	tokenData := map[string]interface{}{
		"access_token": "tok_9876543210abc",
		"token_type":   "Bearer",
		"expires_in":   600,
	}
	oauth := &OAuth2Stub{ClientID: clientID, Token: tokenData}
	header := oauth.AuthHeader()
	assert.True(t, strings.HasPrefix(header, "Bearer "))
	assert.Contains(t, header, "tok_9876543210abc")
}

func TestPublicOAuth2AuthReprDiff(t *testing.T) {
	oauth := &OAuth2Stub{ClientID: "public_id", Token: nil}
	rep := "OAuth2(" + oauth.ClientID + ")"
	assert.Contains(t, rep, "public_id")
	assert.True(t, strings.HasPrefix(rep, "OAuth2("))
}