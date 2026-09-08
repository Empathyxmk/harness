package tests

import (
	"net"
	"net/url"
	"strings"
	"testing"

	"golang.org/x/net/idna"
	"github.com/stretchr/testify/assert"
)

// PunycodeURLNormalizer is a test helper for simulating URL normalization
type PunycodeURLNormalizer struct{}

func (n *PunycodeURLNormalizer) Filter(_ interface{}, _ interface{}, urlStr string) string {
	parsed, err := url.Parse(urlStr)
	if err != nil || parsed.Host == "" {
		return ""
	}
	hostASCII, err := idna.ToASCII(parsed.Host)
	if err != nil {
		return ""
	}
	parsed.Host = hostASCII
	return parsed.String()
}

func TestAsciiURL(t *testing.T) {
	urlStr := "http://example.com"
	n := &PunycodeURLNormalizer{}
	assert.Equal(t, urlStr, n.Filter(nil, nil, urlStr))
}

func TestPunycodeURL(t *testing.T) {
	// Japanese for "example": 例え.テスト
	urlStr := "http://例え.テスト"
	n := &PunycodeURLNormalizer{}
	normalized := n.Filter(nil, nil, urlStr)
	assert.True(t, strings.HasPrefix(normalized, "http://xn--r8jz45g.xn--zckzah"))
}

func TestNonHostPartIsNotChanged(t *testing.T) {
	urlStr := "http://täst.de/foo?ä=ö"
	n := &PunycodeURLNormalizer{}
	result := n.Filter(nil, nil, urlStr)
	assert.True(t, strings.HasPrefix(result, "http://xn--tst-qla.de"))
	assert.Contains(t, result, "/foo")
	assert.Contains(t, result, "?")
}

func TestMalformedURL(t *testing.T) {
	urlStr := "not a url"
	n := &PunycodeURLNormalizer{}
	assert.Equal(t, "", n.Filter(nil, nil, urlStr))
}

func TestHostAlreadyPunycode(t *testing.T) {
	puny := "http://xn--fsq.xn--0zwm56d"
	n := &PunycodeURLNormalizer{}
	assert.Equal(t, puny, n.Filter(nil, nil, puny))
}