package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class UrlsPublicTest {

    @Test
    public void testIsWebSchemeWithHttp_public() {
        assertTrue(Urls.isWebScheme("http://floo.io"));
    }

    @Test
    public void testIsWebSchemeWithCustomScheme_public() {
        assertFalse(Urls.isWebScheme("notweb://example.org"));
    }

    @Test
    public void testCombine_public() {
        assertEquals("foo://bar/baz", Urls.combine("foo://bar", "baz"));
    }
}