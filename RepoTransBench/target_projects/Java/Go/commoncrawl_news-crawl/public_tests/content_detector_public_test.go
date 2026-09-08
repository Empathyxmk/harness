package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type ContentDetector struct{}

func (c *ContentDetector) IsNewsContent(input string) bool {
	if strings.Contains(strings.ToLower(input), "news") && strings.Contains(input, "<article>") {
		return true
	}
	return false
}

func TestDetectsContentHtmlNews(t *testing.T) {
	detector := &ContentDetector{}
	html := "<html><head><title>Breaking World News</title></head><body><article>Some News</article></body></html>"
	assert.True(t, detector.IsNewsContent(html))
}

func TestNonNewsContent(t *testing.T) {
	detector := &ContentDetector{}
	html := "<html><head><title>Shopping Cart</title></head><body>Item list</body></html>"
	assert.False(t, detector.IsNewsContent(html))
}

func TestRealisticBlogContent(t *testing.T) {
	detector := &ContentDetector{}
	html := "<html><body><div class=\"blog-post\">Personal story from travel</div></body></html>"
	assert.False(t, detector.IsNewsContent(html))
}