package tests

import (
	"bytes"
	"testing"

	"medium-sdk-go/medium"
)

// Helper for comparing slices
func stringSlicesEqual(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}

func TestExchangeAuthorizationCode(t *testing.T) {
	mockDo := func(payload map[string][]string) (int, map[string]interface{}) {
		if payload["code"][0] != "mycode" {
			t.Errorf("Expected code=mycode, got %v", payload["code"][0])
		}
		if payload["client_id"][0] != "myclientid" {
			t.Errorf("Expected client_id=myclientid, got %v", payload["client_id"][0])
		}
		if payload["client_secret"][0] != "myclientsecret" {
			t.Errorf("Expected client_secret=myclientsecret, got %v", payload["client_secret"][0])
		}
		if payload["grant_type"][0] != "authorization_code" {
			t.Errorf("Expected grant_type=authorization_code, got %v", payload["grant_type"][0])
		}
		if payload["redirect_uri"][0] != "http://example.com/cb" {
			t.Errorf("Expected redirect_uri=http://example.com/cb, got %v", payload["redirect_uri"][0])
		}
		resp := map[string]interface{}{
			"token_type":    "Bearer",
			"access_token":  "myaccesstoken",
			"expires_at":    4575744000000,
			"refresh_token": "myrefreshtoken",
			"scope":         []string{"basicProfile"},
		}
		return 201, resp
	}
	client := medium.NewClientWithCreds("myclientid", "myclientsecret", "")
	resp, err := client.ExchangeAuthorizationCode("mycode", "http://example.com/cb", mockDo)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if resp["access_token"].(string) != "myaccesstoken" {
		t.Errorf("Expected access_token=myaccesstoken, got %v", resp["access_token"])
	}
	if resp["refresh_token"].(string) != "myrefreshtoken" {
		t.Errorf("Expected refresh_token=myrefreshtoken, got %v", resp["refresh_token"])
	}
	scope, ok := resp["scope"].([]string)
	if !ok {
		raw := resp["scope"]
		if slc, ok := raw.([]interface{}); ok {
			scope = make([]string, len(slc))
			for i, v := range slc {
				scope[i] = v.(string)
			}
		}
	}
	if !stringSlicesEqual(scope, []string{"basicProfile"}) {
		t.Errorf("Expected scope [basicProfile], got %+v", scope)
	}
}

func TestExchangeRefreshToken(t *testing.T) {
	mockDo := func(payload map[string][]string) (int, map[string]interface{}) {
		if payload["refresh_token"][0] != "myrefreshtoken" {
			t.Errorf("Expected refresh_token=myrefreshtoken, got %v", payload["refresh_token"][0])
		}
		if payload["client_id"][0] != "myclientid" {
			t.Errorf("Expected client_id=myclientid, got %v", payload["client_id"][0])
		}
		if payload["client_secret"][0] != "myclientsecret" {
			t.Errorf("Expected client_secret=myclientsecret, got %v", payload["client_secret"][0])
		}
		if payload["grant_type"][0] != "refresh_token" {
			t.Errorf("Expected grant_type=refresh_token, got %v", payload["grant_type"][0])
		}
		resp := map[string]interface{}{
			"token_type":    "Bearer",
			"access_token":  "myaccesstoken2",
			"expires_at":    4575744000000,
			"refresh_token": "myrefreshtoken2",
			"scope":         []string{"basicProfile"},
		}
		return 201, resp
	}
	client := medium.NewClientWithCreds("myclientid", "myclientsecret", "")
	resp, err := client.ExchangeRefreshToken("myrefreshtoken", mockDo)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	if resp["access_token"].(string) != "myaccesstoken2" {
		t.Errorf("Expected access_token=myaccesstoken2, got %v", resp["access_token"])
	}
	if resp["refresh_token"].(string) != "myrefreshtoken2" {
		t.Errorf("Expected refresh_token=myrefreshtoken2, got %v", resp["refresh_token"])
	}
	scope, ok := resp["scope"].([]string)
	if !ok {
		raw := resp["scope"]
		if slc, ok := raw.([]interface{}); ok {
			scope = make([]string, len(slc))
			for i, v := range slc {
				scope[i] = v.(string)
			}
		}
	}
	if !stringSlicesEqual(scope, []string{"basicProfile"}) {
		t.Errorf("Expected scope [basicProfile], got %+v", scope)
	}
}

func TestGetCurrentUser(t *testing.T) {
	mockDo := func(_ map[string][]string) (int, map[string]interface{}) {
		resp := map[string]interface{}{
			"username":  "nicki",
			"url":       "https://medium.com/@nicki",
			"imageUrl":  "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png",
			"id":        "5303d74c64f66366f00cb9b2a94f3251bf5",
			"name":      "Nicki Minaj",
		}
		return 200, resp
	}
	client := medium.NewClient("myaccesstoken")
	got, err := client.GetCurrentUser(mockDo)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	expected := map[string]interface{}{
		"username":  "nicki",
		"url":       "https://medium.com/@nicki",
		"imageUrl":  "https://images.medium.com/0*fkfQiTzT7TlUGGyI.png",
		"id":        "5303d74c64f66366f00cb9b2a94f3251bf5",
		"name":      "Nicki Minaj",
	}
	for k, v := range expected {
		if got[k] != v {
			t.Errorf("Expected property %s=%v, got %v", k, v, got[k])
		}
	}
}

func TestCreatePost(t *testing.T) {
	mockDo := func(payload map[string]interface{}) (int, map[string]interface{}) {
		expected := map[string]interface{}{
			"title":         "Starships",
			"content":       "<p>Are meant to flyyyy</p>",
			"contentFormat": "html",
			"tags":          []string{"stars", "ships", "pop"},
			"publishStatus": "draft",
		}
		// Check fields of payload
		for k, v := range expected {
			switch val := v.(type) {
			case []string:
				payloadVal, _ := payload[k].([]string)
				if !stringSlicesEqual(payloadVal, val) {
					t.Errorf("Expected %s = %v, got %v", k, val, payloadVal)
				}
			case string:
				if payload[k] != val {
					t.Errorf("Expected %s = %v, got %v", k, val, payload[k])
				}
			}
		}
		resp := map[string]interface{}{
			"license":      "all-rights-reserved",
			"title":        "Starships",
			"url":          "https://medium.com/@nicki/55050649c95",
			"tags":         []string{"stars", "ships", "pop"},
			"authorId":     "5303d74c64f66366f00cb9b2a94f3251bf5",
			"publishStatus":"draft",
			"id":           "55050649c95",
		}
		return 200, resp
	}
	client := medium.NewClient("myaccesstoken")
	resp, err := client.CreatePost(
		"5303d74c64f66366f00cb9b2a94f3251bf5",
		"Starships",
		"<p>Are meant to flyyyy</p>",
		"html",
		[]string{"stars", "ships", "pop"},
		"draft",
		mockDo,
	)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	expected := map[string]interface{}{
		"license":      "all-rights-reserved",
		"title":        "Starships",
		"url":          "https://medium.com/@nicki/55050649c95",
		"tags":         []string{"stars", "ships", "pop"},
		"authorId":     "5303d74c64f66366f00cb9b2a94f3251bf5",
		"publishStatus":"draft",
		"id":           "55050649c95",
	}
	for k, v := range expected {
		switch val := v.(type) {
		case []string:
			got, _ := resp[k].([]string)
			if !stringSlicesEqual(got, val) {
				t.Errorf("Expected %s=%v, got %v", k, val, got)
			}
		case string:
			if resp[k] != val {
				t.Errorf("Expected %s=%v, got %v", k, val, resp[k])
			}
		}
	}
}

func TestUploadImage(t *testing.T) {
	mockDo := func(req *medium.MockUploadReq) (int, map[string]interface{}) {
		if req.Headers["Authorization"] != "Bearer myaccesstoken" {
			t.Errorf("Expected header Authorization='Bearer myaccesstoken', got '%s'", req.Headers["Authorization"])
		}
		if !bytes.Contains(req.Body, []byte("Content-Type: image/png")) {
			t.Errorf("Expected request body to include 'Content-Type: image/png', got %s", string(req.Body))
		}
		resp := map[string]interface{}{
			"url": "https://cdn-images-1.medium.com/0*dlkfjalksdjfl.jpg",
			"md5": "d87e1628ca597d386e8b3e25de3a18bc",
		}
		return 200, resp
	}
	client := medium.NewClientWithCreds("", "", "myaccesstoken")
	resp, err := client.UploadImage("./tests/test.png", "image/png", mockDo)
	if err != nil {
		t.Fatalf("Unexpected error: %v", err)
	}
	expected := map[string]interface{}{
		"url": "https://cdn-images-1.medium.com/0*dlkfjalksdjfl.jpg",
		"md5": "d87e1628ca597d386e8b3e25de3a18bc",
	}
	for k, v := range expected {
		if resp[k] != v {
			t.Errorf("Expected %s=%v, got %v", k, v, resp[k])
		}
	}
}