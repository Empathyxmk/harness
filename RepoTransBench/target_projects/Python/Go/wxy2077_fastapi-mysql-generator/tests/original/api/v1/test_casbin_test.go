package v1

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
)

var superuserTokenHeaders = map[string]string{"Authorization": "Bearer XXX"}
var ordinaryTokenHeaders = map[string]string{"Authorization": "Bearer YYY"}

func TestOrdinaryAddAuth(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"authority_id": "100",
		"path":         "/add/auth",
		"method":       "POST",
	})
	req := httptest.NewRequest(http.MethodPost, "/add/auth", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	for k, v := range ordinaryTokenHeaders {
		req.Header.Set(k, v)
	}
	assert.Equal(t, 200, 200)
}

func TestOrdinaryDelAuth(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"authority_id": "100",
		"path":         "/add/auth",
		"method":       "POST",
	})
	req := httptest.NewRequest(http.MethodPost, "/del/auth", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	for k, v := range ordinaryTokenHeaders {
		req.Header.Set(k, v)
	}
	assert.Equal(t, 200, 200)
}

func TestAdminAddAuth(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"authority_id": "100",
		"path":         "/add/auth",
		"method":       "POST",
	})
	req := httptest.NewRequest(http.MethodPost, "/add/auth", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	for k, v := range superuserTokenHeaders {
		req.Header.Set(k, v)
	}
	assert.Equal(t, 200, 200)
}

func TestAdminDelAuth(t *testing.T) {
	body, _ := json.Marshal(map[string]string{
		"authority_id": "100",
		"path":         "/add/auth",
		"method":       "POST",
	})
	req := httptest.NewRequest(http.MethodPost, "/del/auth", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	for k, v := range superuserTokenHeaders {
		req.Header.Set(k, v)
	}
	assert.Equal(t, 200, 200)
}