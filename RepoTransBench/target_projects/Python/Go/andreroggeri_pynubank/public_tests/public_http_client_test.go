package public_tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

type HttpClientPublic struct {
	headers  map[string]string
	base_url string
}

func NewHttpClientPublic() *HttpClientPublic {
	return &HttpClientPublic{headers: make(map[string]string)}
}

func (c *HttpClientPublic) SetHeader(key, value string) {
	c.headers[key] = value
}
func (c *HttpClientPublic) RemoveHeader(key string) {
	delete(c.headers, key)
}
func (c *HttpClientPublic) BaseUrl() string {
	return c.base_url
}
func (c *HttpClientPublic) SetBaseUrl(u string) {
	c.base_url = u
}
func (c *HttpClientPublic) String() string {
	return "HttpClient"
}

func TestHttpClientHeadersPublic(t *testing.T) {
	client := NewHttpClientPublic()
	client.SetHeader("X-Custom-Header", "foobar-public")
	assert.Equal(t, "foobar-public", client.headers["X-Custom-Header"])
	client.RemoveHeader("X-Custom-Header")
	_, ok := client.headers["X-Custom-Header"]
	assert.False(t, ok)
}

func TestHttpClientBaseUrlPublic(t *testing.T) {
	client := NewHttpClientPublic()
	client.SetBaseUrl("https://public.example.com")
	assert.Contains(t, client.BaseUrl(), "https://")
}

func TestHttpClientReprPublic(t *testing.T) {
	client := NewHttpClientPublic()
	r := client.String()
	assert.Contains(t, r, "HttpClient")
}