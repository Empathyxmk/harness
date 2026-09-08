package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.List;

public class NewsSiteMapParserPublicTest {

    @Test
    public void testParseAlternativeSitemap() {
        NewsSiteMapParser parser = new NewsSiteMapParser();
        String xml = "<?xml version=\"1.0\"?><urlset><url><loc>http://different.com/news/1</loc></url><url><loc>http://different.com/news/2</loc></url></urlset>";
        List<String> urls = parser.parse(xml);
        assertTrue(urls.contains("http://different.com/news/1"));
        assertTrue(urls.contains("http://different.com/news/2"));
        assertEquals(2, urls.size());
    }

    @Test
    public void testParseNewsSitemapWithNamespace() {
        NewsSiteMapParser parser = new NewsSiteMapParser();
        String xml = "<?xml version=\"1.0\"?><urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"><url><loc>http://site.org/latest/45</loc></url></urlset>";
        List<String> urls = parser.parse(xml);
        assertTrue(urls.contains("http://site.org/latest/45"));
        assertEquals(1, urls.size());
    }

    @Test
    public void testEmptySitemap() {
        NewsSiteMapParser parser = new NewsSiteMapParser();
        String xml = "<?xml version=\"1.0\"?><urlset></urlset>";
        List<String> urls = parser.parse(xml);
        assertNotNull(urls);
        assertTrue(urls.isEmpty());
    }
}