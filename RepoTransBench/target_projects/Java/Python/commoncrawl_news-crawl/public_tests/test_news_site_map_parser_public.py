import xml.etree.ElementTree as ET

def parse(xml):
    # Extract all <loc> elements in a urlset, ignoring namespaces
    urls = []
    try:
        root = ET.fromstring(xml)
        for url in root.findall(".//url"):
            loc = url.find("loc")
            if loc is not None:
                urls.append(loc.text)
        # Try namespace-aware search as well, for robustness
        if not urls:
            for url in root.findall(".//{*}url"):
                loc = url.find('{*}loc')
                if loc is not None:
                    urls.append(loc.text)
    except Exception:
        pass
    return urls

def test_parse_alternative_sitemap():
    xml = "<?xml version=\"1.0\"?><urlset><url><loc>http://different.com/news/1</loc></url><url><loc>http://different.com/news/2</loc></url></urlset>"
    urls = parse(xml)
    assert "http://different.com/news/1" in urls
    assert "http://different.com/news/2" in urls
    assert len(urls) == 2

def test_parse_news_sitemap_with_namespace():
    xml = "<?xml version=\"1.0\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://site.org/latest/45</loc></url></urlset>"
    urls = parse(xml)
    assert "http://site.org/latest/45" in urls
    assert len(urls) == 1

def test_empty_sitemap():
    xml = "<?xml version=\"1.0\"?><urlset></urlset>"
    urls = parse(xml)
    assert urls is not None
    assert len(urls) == 0