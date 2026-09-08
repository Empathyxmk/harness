package public_tests

import (
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type MockHttpClientPublic struct{}

func (c *MockHttpClientPublic) Get(url string) (interface{}, error) {
	if url == "another.invalid.url" {
		return nil, errors.New("NuException")
	}
	return "ok", nil
}
func (c *MockHttpClientPublic) Post(url string, data map[string]interface{}) (interface{}, error) {
	if url == "another.invalid.url" {
		return nil, errors.New("NuException")
	}
	return "ok", nil
}

func TestGetInvalidUrlShouldThrowExceptionPublic(t *testing.T) {
	client := &MockHttpClientPublic{}
	_, err := client.Get("another.invalid.url")
	assert.Error(t, err)
}

func TestPostInvalidUrlShouldThrowExceptionPublic(t *testing.T) {
	client := &MockHttpClientPublic{}
	_, err := client.Post("another.invalid.url", map[string]interface{}{})
	assert.Error(t, err)
}