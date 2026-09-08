def pre_filter(input_dict):
    # Remove URLs that are not 'article' or 'news' in path
    url = input_dict.get('url', '')
    if "/article" in url or "/news" in url:
        return {'url': url}
    return {'url': None}

def test_url_parameter_remains_untouched():
    input = {"url": "http://example.net/article?id=123"}
    filtered = pre_filter(input)
    assert filtered['url'] == "http://example.net/article?id=123"

def test_non_article_url_is_removed():
    input = {"url": "http://example.org/about"}
    filtered = pre_filter(input)
    assert filtered['url'] is None

def test_edge_case_with_unusual_subdomain():
    input = {"url": "http://sub.subdomain.example.edu/path/to/news"}
    filtered = pre_filter(input)
    assert filtered['url'] == "http://sub.subdomain.example.edu/path/to/news"