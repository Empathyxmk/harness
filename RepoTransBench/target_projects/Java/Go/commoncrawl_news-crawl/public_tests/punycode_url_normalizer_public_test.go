package public_tests

import (
	"net/url"
	"strings"
	"testing"

	"golang.org/x/net/idna"
	"github.com/stretchr/testify/assert"
)

type PunycodeURLNormalizer struct{}

func (n *PunycodeURLNormalizer) Normalize(idn string) string {
	parsed, err := url.Parse(idn)
	if err != nil || parsed.Host == "" {
		return idn
	}
	hostASCII, err := idna.ToASCII(parsed.Host)
	if err != nil {
		return idn
	}
	parsed.Host = hostASCII
	return parsed.String()
}

func TestNormalizerDifferentIDN(t *testing.T) {
	normalizer := &PunycodeURLNormalizer{}
	idn := "http://müller.de/über-uns"
	expected := "http://xn--mller-kva.de/%C3%BCber-uns"
	assert.Equal(t, expected, normalizer.Normalize(idn))
}

func TestNormalizerJapaneseDomain(t *testing.T) {
	normalizer := &PunycodeURLNormalizer{}
	idn := "http://例え.テスト"
	expected := "http://xn--r8jz45g.xn--zckzah"
	actual := normalizer.Normalize(idn)
	assert.True(t, strings.HasPrefix(actual, expected))
}

func TestNormalizerNonIDN(t *testing.T) {
	normalizer := &PunycodeURLNormalizer{}
	url := "http://standard.net/news"
	assert.Equal(t, url, normalizer.Normalize(url))
}