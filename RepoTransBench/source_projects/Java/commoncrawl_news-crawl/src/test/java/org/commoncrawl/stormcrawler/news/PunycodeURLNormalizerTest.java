package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;

public class PunycodeURLNormalizerTest {

    private static final PunycodeURLNormalizer normalizer = new PunycodeURLNormalizer();

    @Test
    public void testAsciiURL() {
        String url = "http://example.com";
        assertEquals(url, normalizer.filter(null, null, url));
    }

    @Test
    public void testPunycodeURL() {
        // Japanese for "example": 例え.テスト
        String url = "http://例え.テスト";
        String normalized = normalizer.filter(null, null, url);
        assertTrue(normalized.startsWith("http://xn--r8jz45g.xn--zckzah"));
    }

    @Test
    public void testNonHostPartIsNotChanged() {
        String url = "http://täst.de/foo?ä=ö";
        String result = normalizer.filter(null, null, url);
        assertTrue(result.startsWith("http://xn--tst-qla.de"));
        assertTrue(result.contains("/foo"));
        assertTrue(result.contains("?"));
    }

    @Test
    public void testMalformedURL() {
        String url = "not a url";
        assertNull(normalizer.filter(null, null, url));
    }

    @Test
    public void testHostAlreadyPunycode() {
        String puny = "http://xn--fsq.xn--0zwm56d";
        assertEquals(puny, normalizer.filter(null, null, puny));
    }
}