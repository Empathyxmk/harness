package public_tests

import (
	"encoding/xml"
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type NewsSiteMapParser struct{}

func (p *NewsSiteMapParser) Parse(xmlStr string) []string {
	type Url struct {
		Loc string `xml:"loc"`
	}
	type Urlset struct {
		URLs []Url `xml:"url"`
	}
	decoder := xml.NewDecoder(strings.NewReader(xmlStr))
	var us Urlset
	err := decoder.Decode(&us)
	if err != nil {
		return []string{}
	}
	results := []string{}
	for _, u := range us.URLs {
		results = append(results, u.Loc)
	}
	return results
}

func TestParseAlternativeSitemap(t *testing.T) {
	parser := &NewsSiteMapParser{}
	xmlstr := `<?xml version="1.0"?><urlset><url><loc>http://different.com/news/1</loc></url><url><loc>http://different.com/news/2</loc></url></urlset>`
	urls := parser.Parse(xmlstr)
	assert.Contains(t, urls, "http://different.com/news/1")
	assert.Contains(t, urls, "http://different.com/news/2")
	assert.Equal(t, 2, len(urls))
}

func TestParseNewsSitemapWithNamespace(t *testing.T) {
	parser := &NewsSiteMapParser{}
	xmlstr := `<?xml version="1.0"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>http://site.org/latest/45</loc></url></urlset>`
	urls := parser.Parse(xmlstr)
	assert.Contains(t, urls, "http://site.org/latest/45")
	assert.Equal(t, 1, len(urls))
}

func TestEmptySitemap(t *testing.T) {
	parser := &NewsSiteMapParser{}
	xmlstr := `<?xml version="1.0"?><urlset></urlset>`
	urls := parser.Parse(xmlstr)
	assert.NotNil(t, urls)
	assert.True(t, len(urls) == 0)
}