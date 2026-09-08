def is_news_content(html):
    # Simulate detection: if 'news' in title or <article>
    h = html.lower()
    if '<title>' in h and 'news' in h:
        return True
    if '<article>' in h:
        return True
    # If the word 'blog-post' appears, it's non-news
    if 'blog-post' in h:
        return False
    return False

def test_detects_content_html_news():
    html = "<html><head><title>Breaking World News</title></head><body><article>Some News</article></body></html>"
    assert is_news_content(html) is True

def test_non_news_content():
    html = "<html><head><title>Shopping Cart</title></head><body>Item list</body></html>"
    assert is_news_content(html) is False

def test_realistic_blog_content():
    html = "<html><body><div class=\"blog-post\">Personal story from travel</div></body></html>"
    assert is_news_content(html) is False