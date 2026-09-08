package original

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockHttpClient struct{}

func (c *MockHttpClient) Get(url string) (interface{}, error) {
	if url == "invalid.url" {
		return nil, errors.New("NuException")
	}
	return "ok", nil
}
func (c *MockHttpClient) Post(url string, data map[string]interface{}) (interface{}, error) {
	if url == "invalid.url" {
		return nil, errors.New("NuException")
	}
	return "ok", nil
}

func TestGetInvalidUrlShouldThrowException(t *testing.T) {
	client := &MockHttpClient{}
	_, err := client.Get("invalid.url")
	assert.Error(t, err)
}

func TestPostInvalidUrlShouldThrowException(t *testing.T) {
	client := &MockHttpClient{}
	_, err := client.Post("invalid.url", map[string]interface{}{})
	assert.Error(t, err)
}