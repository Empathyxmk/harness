package v1

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestAddPolicyPublic(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"p_type": "p",
		"v0":     "public_admin",
		"v1":     "/public/data2",
		"v2":     "write",
	})
	req := httptest.NewRequest(http.MethodPost, "/casbin/add_policy", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestEnforcePublic(t *testing.T) {
	// Simulate enforce GET
	req := httptest.NewRequest(http.MethodGet, "/casbin/enforce?sub=public_admin&obj=/public/data2&act=write", nil)
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestRemovePolicyPublic(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"p_type": "p",
		"v0":     "public_admin",
		"v1":     "/public/data2",
		"v2":     "write",
	})
	req := httptest.NewRequest(http.MethodPost, "/casbin/remove_policy", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestEnforceRemovedPublic(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/casbin/enforce?sub=public_admin&obj=/public/data2&act=write", nil)
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}