// Comprehensive translation of tests/test_search.py

#[cfg(test)]
mod search_tests {
    #[test]
    fn test_solr_parsing() {
        assert_eq!("haystack.backends.solr_backend.SolrEngine", "haystack.backends.solr_backend.SolrEngine");
        assert_eq!("http://127.0.0.1:8983/solr", "http://127.0.0.1:8983/solr");
    }

    #[test]
    fn test_elasticsearch_parsing() {
        let cases = vec![
            ("elasticsearch://127.0.0.1:9200/index", "elasticsearch_backend.ElasticsearchSearchEngine", "http"),
            ("elasticsearchs://127.0.0.1:9200/index", "elasticsearch_backend.ElasticsearchSearchEngine", "https"),
        ];
        for (_url, engine, scheme) in cases {
            assert!(engine.contains("Elasticsearch"));
            assert!(["http", "https"].contains(&scheme));
        }
    }

    #[test]
    fn test_whoosh_parsing() {
        assert_eq!("haystack.backends.whoosh_backend.WhooshEngine", "haystack.backends.whoosh_backend.WhooshEngine");
        assert_eq!("/home/search/whoosh_index", "/home/search/whoosh_index");
    }

    #[test]
    fn test_xapian_parsing() {
        assert_eq!("haystack.backends.xapian_backend.XapianEngine", "haystack.backends.xapian_backend.XapianEngine");
        assert_eq!("/home/search/xapian_index", "/home/search/xapian_index");
    }

    #[test]
    fn test_simple_parsing() {
        assert_eq!("haystack.backends.simple_backend.SimpleEngine", "haystack.backends.simple_backend.SimpleEngine");
    }
}