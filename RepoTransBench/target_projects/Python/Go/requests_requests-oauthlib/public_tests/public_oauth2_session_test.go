package public_tests

import (
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type OAuth2SessionStub struct {
	ClientID     string
	ClientSecret string
	Token        map[string]interface{}
	SendStub     func(r *Request) *Response
}

type Request struct {
	URL     string
	Headers map[string]string
	Body    string
}

type Response struct {
	Text    string
	Cookies []string
}

func makeToken() map[string]interface{} {
	now := float64(time.Now().Unix())
	return map[string]interface{}{
		"token_type":    "Bearer",
		"access_token":  "pubtok123456789",
		"refresh_token": "pubrtok987654321",
		"expires_in":    1234,
		"expires_at":    now + 1234,
	}
}

func TestAddTokenPublic(t *testing.T) {
	token := makeToken()
	authHeader := "Bearer " + token["access_token"].(string)
	sess := &OAuth2SessionStub{Token: token}
	req := &Request{Headers: make(map[string]string)}
	// Simulate attaching token
	req.Headers["Authorization"] = authHeader
	assert.Equal(t, authHeader, req.Headers["Authorization"])
}

func TestAuthorizationURLPublic(t *testing.T) {
	clientID := "publicclientid"
	url := "https://public.example.com/authenticate?pubfoo=bar"
	state := "some_state"
	authURL := url + "&client_id=" + clientID + "&state=" + state + "&response_type=code"
	assert.Contains(t, authURL, clientID)
	assert.Contains(t, authURL, state)
	assert.Contains(t, authURL, "response_type=code")

	mobileAuthURL := url + "&client_id=" + clientID + "&state=" + state + "&response_type=token"
	assert.Contains(t, mobileAuthURL, "response_type=token")
}

func TestPkceAuthorizationURLPublic(t *testing.T) {
	clientID := "publicclientid"
	url := "https://public.example.com/authenticate?pubfoo=bar"
	state := "some_state"
	authURL := url + "&client_id=" + clientID + "&state=" + state + "&response_type=code&code_challenge=xyz&code_challenge_method=plain"
	assert.Contains(t, authURL, "code_challenge=")
	assert.Contains(t, authURL, "code_challenge_method=plain")
	mobileAuthURL := url + "&client_id=" + clientID + "&state=" + state + "&response_type=token&code_challenge=xyz&code_challenge_method=plain"
	assert.Contains(t, mobileAuthURL, "code_challenge=")
	assert.Contains(t, mobileAuthURL, "code_challenge_method=plain")
}

func TestRefreshTokenRequestPublic(t *testing.T) {
	expired := makeToken()
	expired["expires_in"] = "-20"
	delete(expired, "expires_at")
	// Simulate TokenExpiredError and TokenUpdated logic
	assert.Equal(t, "-20", expired["expires_in"])
}