import pytest
import xml.etree.ElementTree as ET
import datetime
import io

class SitemapType:
    # Simulating types from Java enum
    NEWS = "NEWS"
    UNKNOWN = "UNKNOWN"

class Outlink:
    def __init__(self, url):
        self.url = url

class NewsSiteMapParserBolt:
    def __init__(self):
        self.filter_hours_since_modified = 168  # default one week
        self.sniff_content = True

    def prepare(self, config, context, collector):
        self.filter_hours_since_modified = config.get("sitemap.filter.hours.since.modified", 168)
        self.sniff_content = config.get("sitemap.sniffContent", True)
        self.collector = collector

    def detectContent(self, url, content_bytes):
        # Very primitive: just detect <news:news> tag
        content = content_bytes.decode('utf-8', errors='ignore')
        if "<news:news>" in content:
            return SitemapType.NEWS
        return SitemapType.UNKNOWN

    def parseSiteMap(self, url, content_bytes, content_type, parent_metadata, links):
        # The test is based around news sitemaps and publication_date test
        content = content_bytes.decode('utf-8', errors='ignore')
        tree = ET.ElementTree(ET.fromstring(content))
        root = tree.getroot()
        latest_date = None
        for url_element in root.findall(".//url"):
            # Check for <news:publication_date> in the children
            pub_date_elem = url_element.find(".//{*}publication_date")
            loc_elem = url_element.find(".//loc")
            if loc_elem is None or pub_date_elem is None:
                continue
            pub_date = pub_date_elem.text
            # parse date; skip if too old
            pub_date_obj = datetime.datetime.strptime(pub_date, "%Y-%m-%d")
            now = datetime.datetime.now()
            diff = now - pub_date_obj
            if diff.total_seconds() > self.filter_hours_since_modified * 3600:
                continue
            # Add main loc link
            links.append(Outlink(loc_elem.text))
            # look for xhtml:link elements
            for xe in url_element.findall(".//{*}link"):
                href = xe.attrib.get('href')
                if href:
                    links.append(Outlink(href))

class FakeCollector:
    def __init__(self):
        self.emitted = []

    def emit(self, *args):
        self.emitted.append(args)

@pytest.fixture
def parser_bolt():
    bolt = NewsSiteMapParserBolt()
    config = {"sitemap.sniffContent": True, "sitemap.filter.hours.since.modified": 168}
    bolt.prepare(config, None, FakeCollector())
    return bolt

def read_content(filename='tests/resources/sitemap-news.xml'):
    # Contents should match the test resource example, using an inline minimum valid XML
    # Here, the date <news:publication_date>2008-12-23</news:publication_date> will be used for first parse
    # The structure matches the minimal Java sample.
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url>
    <loc>https://example.org/news/1</loc>
    <news:news>
      <news:publication>
        <news:name>Example</news:name>
        <news:language>en</news:language>
      </news:publication>
      <news:title>Example News Title</news:title>
      <news:publication_date>2008-12-23</news:publication_date>
    </news:news>
    <xhtml:link rel="alternate" media="only screen and (max-width: 640px)" href="https://example.org/mobile/1"/>
    <image:image>
      <image:loc>https://example.org/news/1/image.jpg</image:loc>
    </image:image>
  </url>
</urlset>
"""

def test_site_map_parser(parser_bolt):
    url = "https://example.org/sitemap-news.xml"
    content = read_content()
    content_type = ""
    parent_metadata = {}
    links = []

    typ = parser_bolt.detectContent(url, content)
    assert typ == SitemapType.NEWS

    parser_bolt.parseSiteMap(url, content, content_type, parent_metadata, links)
    # original publication date is 2008-12-23, should be skipped
    assert len(links) == 0

    # Now change publication date to yesterday; links should show up
    import datetime
    today = datetime.datetime.now()
    yesterday = (today - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    content_str = content.decode('utf-8').replace(
        "<news:publication_date>2008-12-23</news:publication_date>",
        f"<news:publication_date>{yesterday}</news:publication_date>"
    )
    links_new = []
    parser_bolt.parseSiteMap(url, content_str.encode('utf-8'), content_type, parent_metadata, links_new)
    # one loc link + 1 xhtml:link (ignore image)
    assert len(links_new) == 2