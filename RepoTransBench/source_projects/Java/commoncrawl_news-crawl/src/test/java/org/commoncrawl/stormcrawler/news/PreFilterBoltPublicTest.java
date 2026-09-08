package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;
import java.util.HashMap;
import java.util.Map;

public class PreFilterBoltPublicTest {

    @Test
    public void testUrlParameterRemainsUntouched() {
        PreFilterBolt bolt = new PreFilterBolt();
        Map<String, String> input = new HashMap<>();
        input.put("url", "http://example.net/article?id=123");
        Map<String, String> filtered = bolt.preFilter(input);
        assertEquals("http://example.net/article?id=123", filtered.get("url"));
    }

    @Test
    public void testNonArticleUrlIsRemoved() {
        PreFilterBolt bolt = new PreFilterBolt();
        Map<String, String> input = new HashMap<>();
        input.put("url", "http://example.org/about");
        Map<String, String> filtered = bolt.preFilter(input);
        assertNull(filtered.get("url"));
    }

    @Test
    public void testEdgeCaseWithUnusualSubdomain() {
        PreFilterBolt bolt = new PreFilterBolt();
        Map<String, String> input = new HashMap<>();
        input.put("url", "http://sub.subdomain.example.edu/path/to/news");
        Map<String, String> filtered = bolt.preFilter(input);
        // Assuming the logic allows '/news' as a valid article path
        assertEquals("http://sub.subdomain.example.edu/path/to/news", filtered.get("url"));
    }
}