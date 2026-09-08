package me.drakeet.floo.sample;

import org.junit.Test;

import static org.junit.Assert.*;

public class URLsPublicTest {

    @Test
    public void testSchemeIsFloo_public() {
        assertEquals("floo", URLs.scheme());
    }

    @Test
    public void testConstants_public() {
        assertNotEquals("https://not-public-url.com", URLs.WEB);
        assertNotEquals("floo://not/public", URLs.NOT_REGISTERED);
        // Using public data but checks that URL.S constants are still correct but using not direct copy value
        // This also ensures the constants still work but do not use same data as original test
        assertTrue(URLs.WEB.startsWith("https://"));
        assertTrue(URLs.NOT_REGISTERED.startsWith("floo://"));
    }
}