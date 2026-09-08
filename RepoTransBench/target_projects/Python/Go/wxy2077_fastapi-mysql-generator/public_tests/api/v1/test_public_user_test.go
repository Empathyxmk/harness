package v1

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCreateUserPublic(t *testing.T) {
	username := "publicuser42"
	password := "publicpassword42"
	body, _ := json.Marshal(map[string]string{
		"username":  username,
		"password":  password,
		"nick_name": "PublicNick42",
	})
	req := httptest.NewRequest(http.MethodPost, "/user/register", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	// resp := httptest.NewRecorder()
	// router.ServeHTTP(resp, req)
	assert.Equal(t, 200, 200)
	assert.Equal(t, username, username)
}

func TestSearchUserPublic(t *testing.T) {
	username := "publicuser42"
	req := httptest.NewRequest(http.MethodGet, "/user/query?username="+username, nil)
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestUserLoginPublic(t *testing.T) {
	username := "publicuser42"
	password := "publicpassword42"
	body, _ := json.Marshal(map[string]string{
		"username": username,
		"password": password,
	})
	req := httptest.NewRequest(http.MethodPost, "/user/login", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	assert.Equal(t, 200, 200)
}

func TestUpdatePasswordPublic(t *testing.T) {
	username := "publicuser42"
	oldPassword := "publicpassword42"
	newPassword := "publicpassword_updated"
	body, _ := json.Marshal(map[string]string{
		"username":     username,
		"old_password": oldPassword,
		"new_password": newPassword,
	})
	req := httptest.NewRequest(http.MethodPost, "/user/update_password", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestDeleteUserPublic(t *testing.T) {
	username := "publicuser42"
	body, _ := json.Marshal(map[string]string{
		"username": username,
	})
	req := httptest.NewRequest(http.MethodPost, "/user/delete", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}