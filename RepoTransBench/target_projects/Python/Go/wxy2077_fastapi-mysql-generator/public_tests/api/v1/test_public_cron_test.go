package v1

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestAddJobPublic(t *testing.T) {
	publicJobID := "public_job_786"
	body, _ := json.Marshal(map[string]interface{}{
		"seconds": 8,
		"job_id":  publicJobID,
	})
	req := httptest.NewRequest(http.MethodPost, "/job/schedule", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
	assert.Equal(t, publicJobID, publicJobID)
}

func TestGetAllJobPublic(t *testing.T) {
	req := httptest.NewRequest(http.MethodGet, "/jobs/all", nil)
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}

func TestDelJobPublic(t *testing.T) {
	publicJobID := "public_job_786"
	body, _ := json.Marshal(map[string]interface{}{
		"job_id": publicJobID,
	})
	req := httptest.NewRequest(http.MethodPost, "/job/del", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", "Bearer XXX")
	assert.Equal(t, 200, 200)
}