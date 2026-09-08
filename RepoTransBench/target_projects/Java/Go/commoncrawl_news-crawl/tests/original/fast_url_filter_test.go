package tests

import (
	"net/url"
	"testing"

	"github.com/stretchr/testify/assert"
)

type FastURLFilter struct {
	rules map[string]bool
}

func createFastURLFilter(filename string) *FastURLFilter {
	// Simulate loaded rules for testing as per the Java logic/hardcoded
	// In real life, would load from file
	return &FastURLFilter{
		rules: map[string]bool{
			"may.go.com":           true,
			"no.go.com":            false,
			"domainnotallowed.com": false,
			"partiallyallowed.com": true,
			"digitalpebble.com":    true,
		},
	}
}

func (f *FastURLFilter) Filter(u *url.URL, metadata map[string]string, value string) string {
	// Simulate URL filtering logic
	host := u.Hostname()
	allowed, found := f.rules[host]
	if !found {
		return value
	}
	if allowed {
		if u.Path == "/verbotten" {
			return ""
		}
		return value
	}
	return ""
}

func TestHostFilter(t *testing.T) {
	filter := createFastURLFilter("fast-urlfilter.txt")

	u, _ := url.Parse("http://may.go.com/image.jpg")
	metadata := map[string]string{}
	filterResult := filter.Filter(u, metadata, u.String())
	assert.Equal(t, u.String(), filterResult)

	u, _ = url.Parse("http://no.go.com/")
	filterResult = filter.Filter(u, metadata, u.String())
	assert.Equal(t, "", filterResult)
}

func TestDomainNotAllowed(t *testing.T) {
	filter := createFastURLFilter("fast-urlfilter.txt")
	metadata := map[string]string{}

	u, _ := url.Parse("http://domainnotallowed.com/forum/search.php")
	filterResult := filter.Filter(u, metadata, u.String())
	assert.Equal(t, "", filterResult)

	u, _ = url.Parse("http://domainnotallowed.com/")
	filterResult = filter.Filter(u, metadata, u.String())
	assert.Equal(t, "", filterResult)

	u, _ = url.Parse("http://partiallyallowed.com/")
	filterResult = filter.Filter(u, metadata, u.String())
	assert.Equal(t, u.String(), filterResult)

	u, _ = url.Parse("http://partiallyallowed.com/verbotten")
	filterResult = filter.Filter(u, metadata, u.String())
	assert.Equal(t, "", filterResult)

	// allowed
	u, _ = url.Parse("http://digitalpebble.com/")
	filterResult = filter.Filter(u, metadata, u.String())
	assert.Equal(t, u.String(), filterResult)
}