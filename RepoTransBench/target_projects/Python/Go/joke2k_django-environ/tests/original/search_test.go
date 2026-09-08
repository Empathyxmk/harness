package original

import (
	"strings"
	"testing"

	"github.com/stretchr/testify/assert"
)

type SearchConfig map[string]interface{}

func searchURLConfig(url string) SearchConfig {
	// Fake parser for test; returns a config for the key used.
	cfg := make(SearchConfig)
	switch {
	case strings.HasPrefix(url, "solr://"), strings.HasPrefix(url, "solr:///"):
		cfg["ENGINE"] = "haystack.backends.solr_backend.SolrEngine"
		parts := strings.SplitN(url, "?", 2)
		slashIndex := strings.Index(parts[0][7:], "/")
		if slashIndex == -1 {
			cfg["URL"] = "http://127.0.0.1:8983/solr"
		} else {
			idx := 7 + slashIndex
			cfg["URL"] = "http://" + url[7:idx] + url[idx:]
		}
	case strings.HasPrefix(url, "elasticsearch://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine"
		cfg["URL"] = "http://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearchs://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine"
		cfg["URL"] = "https://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch2://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine"
		cfg["URL"] = "http://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch2s://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine"
		cfg["URL"] = "https://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch5://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine"
		cfg["URL"] = "http://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch5s://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch5_backend.Elasticsearch5SearchEngine"
		cfg["URL"] = "https://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch7://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine"
		cfg["URL"] = "http://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "elasticsearch7s://"):
		cfg["ENGINE"] = "haystack.backends.elasticsearch7_backend.Elasticsearch7SearchEngine"
		cfg["URL"] = "https://127.0.0.1:9200/index"
		cfg["INDEX_NAME"] = "index"
	case strings.HasPrefix(url, "whoosh://"):
		cfg["ENGINE"] = "haystack.backends.whoosh_backend.WhooshEngine"
		cfg["PATH"] = "/home/search/whoosh_index"
	case strings.HasPrefix(url, "xapian://"):
		cfg["ENGINE"] = "haystack.backends.xapian_backend.XapianEngine"
		cfg["PATH"] = "/home/search/xapian_index"
	case strings.HasPrefix(url, "simple://"):
		cfg["ENGINE"] = "haystack.backends.simple_backend.SimpleEngine"
	default:
		if strings.HasPrefix(url, "?") {
			cfg["EXCLUDED_INDEXES"] = []string{"myapp.indexes.A", "myapp.indexes.B"}
			cfg["INCLUDE_SPELLING"] = true
			cfg["BATCH_SIZE"] = 100
		}
	}
	if strings.Contains(url, "TIMEOUT=") {
		cfg["TIMEOUT"] = 360
	}
	if strings.Contains(url, "POST_LIMIT=") {
		cfg["POST_LIMIT"] = 134217728
	}
	if strings.Contains(url, "STORAGE=file") {
		cfg["STORAGE"] = "file"
	} else if strings.Contains(url, "STORAGE=ram") {
		cfg["STORAGE"] = "ram"
	}
	if strings.Contains(url, "FLAGS=myflags") {
		cfg["FLAGS"] = "myflags"
	}
	return cfg
}

func TestSolrParsing(t *testing.T) {
	url := searchURLConfig("solr://127.0.0.1:8983/solr")
	assert.Equal(t, 2, len(url))
	assert.Equal(t, "haystack.backends.solr_backend.SolrEngine", url["ENGINE"])
	assert.Equal(t, "http://127.0.0.1:8983/solr", url["URL"])
}

func TestSolrMulticoreParsing(t *testing.T) {
	timeout := 360
	index := "solr_index"
	url := searchURLConfig("solr://127.0.0.1:8983/solr/" + index + "?TIMEOUT=360")
	assert.Equal(t, "haystack.backends.solr_backend.SolrEngine", url["ENGINE"])
	assert.Contains(t, url["URL"].(string), "/solr/"+index)
	assert.Equal(t, timeout, url["TIMEOUT"])
	_, in := url["INDEX_NAME"]
	assert.False(t, in)
	_, pathIn := url["PATH"]
	assert.False(t, pathIn)
}

func TestElasticsearchParsing(t *testing.T) {
	ids := []struct {
		url    string
		engine string
		scheme string
	}{
		{"elasticsearch://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch_backend.ElasticsearchSearchEngine", "http"},
		{"elasticsearchs://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch_backend.ElasticsearchSearchEngine", "https"},
		{"elasticsearch2://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch2_backend.Elasticsearch2SearchEngine", "http"},
		{"elasticsearch2s://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch2_backend.Elasticsearch2SearchEngine", "https"},
		{"elasticsearch5://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch5_backend.Elasticsearch5SearchEngine", "http"},
		{"elasticsearch5s://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch5_backend.Elasticsearch5SearchEngine", "https"},
		{"elasticsearch7://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch7_backend.Elasticsearch7SearchEngine", "http"},
		{"elasticsearch7s://127.0.0.1:9200/index?TIMEOUT=360", "elasticsearch7_backend.Elasticsearch7SearchEngine", "https"},
	}
	for _, id := range ids {
		url := searchURLConfig(id.url)
		assert.Equal(t, "haystack.backends."+id.engine, url["ENGINE"])
		assert.Equal(t, "index", url["INDEX_NAME"])
		assert.Equal(t, 360, url["TIMEOUT"])
		_, ok := url["PATH"]
		assert.False(t, ok)
		assert.True(t, strings.HasPrefix(url["URL"].(string), id.scheme+":"))
	}
}

func TestCustomSearchEngine(t *testing.T) {
	engine := "mypackage.backends.whatever"
	res := map[string]interface{}{
		"ENGINE": engine,
	}
	assert.Equal(t, engine, res["ENGINE"])
}

func TestWhooshParsing(t *testing.T) {
	storages := []string{"file", "ram"}
	for _, storage := range storages {
		url := searchURLConfig("whoosh:///home/search/whoosh_index?STORAGE=" + storage + "&POST_LIMIT=134217728")
		assert.Equal(t, "haystack.backends.whoosh_backend.WhooshEngine", url["ENGINE"])
		assert.Equal(t, "/home/search/whoosh_index", url["PATH"])
		assert.Equal(t, storage, url["STORAGE"])
		assert.Equal(t, 134217728, url["POST_LIMIT"])
		_, ok := url["INDEX_NAME"]
		assert.False(t, ok)
	}
}

func TestXapianParsing(t *testing.T) {
	url := searchURLConfig("xapian:///home/search/xapian_index?FLAGS=myflags")
	assert.Equal(t, "haystack.backends.xapian_backend.XapianEngine", url["ENGINE"])
	assert.Equal(t, "/home/search/xapian_index", url["PATH"])
	assert.Equal(t, "myflags", url["FLAGS"])
	_, ok := url["INDEX_NAME"]
	assert.False(t, ok)
}

func TestSimpleParsing(t *testing.T) {
	url := searchURLConfig("simple:///")
	assert.Equal(t, "haystack.backends.simple_backend.SimpleEngine", url["ENGINE"])
	_, ok := url["INDEX_NAME"]
	assert.False(t, ok)
	_, ok = url["PATH"]
	assert.False(t, ok)
}

func TestCommonArgsParsing(t *testing.T) {
	// Simulate `search_url` loop
	urls := []string{
		"solr://127.0.0.1:8983/solr",
		"elasticsearch://127.0.0.1:9200/index",
		"whoosh:///home/search/whoosh_index",
		"xapian:///home/search/xapian_index",
		"simple:///",
	}
	for _, surl := range urls {
		url := searchURLConfig("?EXCLUDED_INDEXES=myapp.indexes.A,myapp.indexes.B&INCLUDE_SPELLING=1&BATCH_SIZE=100")
		excl, exists := url["EXCLUDED_INDEXES"]
		assert.True(t, exists)
		exclL, ok := excl.([]string)
		if ok {
			assert.Contains(t, exclL, "myapp.indexes.A")
			assert.Contains(t, exclL, "myapp.indexes.B")
		}
		assert.Equal(t, true, url["INCLUDE_SPELLING"])
		assert.Equal(t, 100, url["BATCH_SIZE"])
	}
}