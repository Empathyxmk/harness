package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type PreFilterBolt struct{}

func (b *PreFilterBolt) PreFilter(input map[string]string) map[string]string {
	out := make(map[string]string)
	url := input["url"]
	if strings.Contains(url, "article") || strings.HasSuffix(url, "/news") {
		out["url"] = url
		return out
	}
	return out
}

func TestUrlParameterRemainsUntouched(t *testing.T) {
	bolt := &PreFilterBolt{}
	input := map[string]string{"url": "http://example.net/article?id=123"}
	filtered := bolt.PreFilter(input)
	assert.Equal(t, "http://example.net/article?id=123", filtered["url"])
}

func TestNonArticleUrlIsRemoved(t *testing.T) {
	bolt := &PreFilterBolt{}
	input := map[string]string{"url": "http://example.org/about"}
	filtered := bolt.PreFilter(input)
	_, ok := filtered["url"]
	assert.False(t, ok)
}

func TestEdgeCaseWithUnusualSubdomain(t *testing.T) {
	bolt := &PreFilterBolt{}
	input := map[string]string{"url": "http://sub.subdomain.example.edu/path/to/news"}
	filtered := bolt.PreFilter(input)
	assert.Equal(t, "http://sub.subdomain.example.edu/path/to/news", filtered["url"])
}