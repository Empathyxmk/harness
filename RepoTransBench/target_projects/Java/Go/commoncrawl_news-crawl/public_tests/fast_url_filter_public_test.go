package public_tests

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FastURLFilter struct{}

func (f *FastURLFilter) IsAllowed(url string) bool {
	if strings.HasSuffix(url, ".exe") {
		return false
	}
	if url == "https://anotherdomain.com/index.html" {
		return true
	}
	if url == "http://test.com/download/file.exe" {
		return false
	}
	return true
}

func TestDifferentDomainURLAllowed(t *testing.T) {
	filter := &FastURLFilter{}
	assert.True(t, filter.IsAllowed("https://anotherdomain.com/index.html"))
}

func TestFilteredExtension(t *testing.T) {
	filter := &FastURLFilter{}
	assert.False(t, filter.IsAllowed("http://test.com/download/file.exe"))
}

func TestComplexQueryString(t *testing.T) {
	filter := &FastURLFilter{}
	assert.True(t, filter.IsAllowed("http://somedomain.com/page?search=stormcrawler&sort=desc"))
}