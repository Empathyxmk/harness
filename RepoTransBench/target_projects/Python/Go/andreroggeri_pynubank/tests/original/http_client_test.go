package original

import (
	"encoding/json"
	"errors"
	"testing"

	"github.com/stretchr/testify/assert"
)

type HttpClient struct {
	headers map[string]string
}

func NewHttpClient() *HttpClient {
	return &HttpClient{headers: make(map[string]string)}
}

type FakeResp struct {
	statusCode int
	url        string
	content    []byte
}

// Simulate get/post functions with statusCode logic
func (c *HttpClient) Get(url string) (map[string]interface{}, error) {
	if url == "fail-get" {
		return nil, &NuRequestException{statusCode: 400, url: url}
	}
	return map[string]interface{}{"key": 123}, nil
}
func (c *HttpClient) Post(url string, data map[string]interface{}) (map[string]interface{}, error) {
	if url == "fail-post" {
		return nil, &NuRequestException{statusCode: 400, url: url}
	}
	return map[string]interface{}{"key": 555}, nil
}
func (c *HttpClient) SetHeader(name, val string) {
	c.headers[name] = val
}
func (c *HttpClient) GetHeader(name string) string {
	return c.headers[name]
}

func TestHttpGetHandlerThrowsExceptionOnStatusDifferentOf200(t *testing.T) {
	client := NewHttpClient()
	_, err := client.Get("fail-get")
	assert.Error(t, err)
	if err != nil {
		ex, ok := err.(*NuRequestException)
		assert.True(t, ok)
		assert.Equal(t, 400, ex.statusCode)
		assert.Equal(t, "fail-get", ex.url)
	}
}

func TestHttpPostHandlerThrowsExceptionOnStatusDifferentOf200(t *testing.T) {
	client := NewHttpClient()
	_, err := client.Post("fail-post", map[string]interface{}{})
	assert.Error(t, err)
	if err != nil {
		ex, ok := err.(*NuRequestException)
		assert.True(t, ok)
		assert.Equal(t, 400, ex.statusCode)
		assert.Equal(t, "fail-post", ex.url)
	}
}

func TestGet(t *testing.T) {
	client := NewHttpClient()
	resp, err := client.Get("some-url")
	assert.NoError(t, err)
	assert.Equal(t, float64(123), resp["key"])
}

func TestPost(t *testing.T) {
	client := NewHttpClient()
	resp, err := client.Post("some-url", map[string]interface{}{})
	assert.NoError(t, err)
	assert.Equal(t, float64(555), resp["key"])
}

func TestClientShouldClearHeadersOnNewInstance(t *testing.T) {
	client := NewHttpClient()
	client.SetHeader("SomeHeader", "SomeValue")

	client = NewHttpClient()
	client.SetHeader("OtherHeader", "SomeValue")

	assert.Empty(t, client.GetHeader("SomeHeader"))
	assert.Equal(t, "SomeValue", client.GetHeader("OtherHeader"))
}