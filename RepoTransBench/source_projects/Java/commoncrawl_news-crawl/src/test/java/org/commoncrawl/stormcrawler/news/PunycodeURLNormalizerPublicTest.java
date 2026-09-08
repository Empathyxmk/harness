package org.commoncrawl.stormcrawler.news;

import org.junit.Test;
import static org.junit.Assert.*;

public class PunycodeURLNormalizerPublicTest {

    @Test
    public void testNormalizerDifferentIDN() {
        PunycodeURLNormalizer normalizer = new PunycodeURLNormalizer();
        String idn = "http://müller.de/über-uns";
        String expected = "http://xn--mller-kva.de/ber-uns";
        assertEquals(expected, normalizer.normalize(idn));
    }

    @Test
    public void testNormalizerJapaneseDomain() {
        PunycodeURLNormalizer normalizer = new PunycodeURLNormalizer();
        String idn = "http://例え.テスト";
        String expected = "http://xn--r8jz45g.xn--zckzah";
        assertEquals(expected, normalizer.normalize(idn));
    }

    @Test
    public void testNormalizerNonIDN() {
        PunycodeURLNormalizer normalizer = new PunycodeURLNormalizer();
        String url = "http://standard.net/news";
        assertEquals(url, normalizer.normalize(url));
    }
}