package tests

import (
	"bytes"
	"encoding/xml"
	"io"
	"os"
	"path/filepath"
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/assert"
)

type SitemapType int

const (
	UnknownSitemap SitemapType = iota
	NewsSitemap
)

type Outlink struct {
	URL string
}

type SitemapNewsEntry struct {
	Loc              string    `xml:"loc"`
	PublicationDate  string    `xml:"news>publication_date"`
	XhtmlLinkHref    string    `xml:"xhtml:link>href,attr"`
	XhtmlLink        string    `xml:"xhtml\\:link>href,attr"`
}

type NewsSiteMapParserBolt struct {
	filterHoursSinceModified int
}

func (b *NewsSiteMapParserBolt) detectContent(url string, content []byte) SitemapType {
	// just basic detection for demo: look for <news: x> inside
	if bytes.Contains(content, []byte("news:publication_date")) {
		return NewsSitemap
	}
	return UnknownSitemap
}

func (b *NewsSiteMapParserBolt) parseSiteMap(
	url string, content []byte, contentType string,
	parentMetadata map[string]string, links *[]Outlink) error {

	// Parse the XML sitemap; expect <urlset><url>...<news:publication_date>...</news:publication_date>...</url></urlset>
	decoder := xml.NewDecoder(bytes.NewReader(content))
	found := false

	for {
		tok, err := decoder.Token()
		if err == io.EOF {
			break
		}
		if err != nil {
			return err
		}
		switch startElem := tok.(type) {
		case xml.StartElement:
			if startElem.Name.Local == "url" {
				var entry struct {
					Loc             string `xml:"loc"`
					PublicationDate string `xml:"news>publication_date"`
					XhtmlLink       string `xml:"xhtml:link>href,attr"`
				}
				if err := decoder.DecodeElement(&entry, &startElem); err == nil {
					if entry.PublicationDate != "" {
						t, _ := time.Parse("2006-01-02", entry.PublicationDate)
						cutoff := time.Now().Add(-time.Duration(b.filterHoursSinceModified) * time.Hour)
						if t.After(cutoff) {
							*links = append(*links, Outlink{URL: entry.Loc})
							if entry.XamlLink != "" {
								*links = append(*links, Outlink{URL: entry.XamlLink})
							}
							found = true
						}
					}
				}
			}
		}
	}
	return nil
}

func readTestResource(filename string) ([]byte, error) {
	path := filepath.Join("tests", "test_resources", filename)
	// fallback for running in project root
	if _, err := os.Stat(path); os.IsNotExist(err) {
		path = filepath.Join("src", "test", "resources", filename)
	}
	return os.ReadFile(path)
}

func TestSiteMapParser(t *testing.T) {
	bolt := &NewsSiteMapParserBolt{filterHoursSinceModified: 168} // 1 week
	url := "https://example.org/sitemap-news.xml"
	content, err := readTestResource("sitemap-news.xml")
	assert.NoError(t, err)
	contentType := ""
	parentMetadata := make(map[string]string)
	links := []Outlink{}

	typ := bolt.detectContent(url, content)
	assert.Equal(t, NewsSitemap, typ)

	err = bolt.parseSiteMap(url, content, contentType, parentMetadata, &links)
	assert.NoError(t, err)
	assert.Equal(t, 0, len(links), "Outdated link not skipped")

	yesterday := time.Now().AddDate(0, 0, -1)
	s := string(content)
	newxml := strings.Replace(s, "<news:publication_date>2008-12-23</news:publication_date>",
		"<news:publication_date>"+yesterday.Format("2006-01-02")+"</news:publication_date>", 1)
	content = []byte(newxml)
	links = nil
	err = bolt.parseSiteMap(url, content, contentType, parentMetadata, &links)
	assert.NoError(t, err)
	assert.Equal(t, 2, len(links), "Expected one <loc> and one additional <xhtml:link> link - image links are ignored")
}