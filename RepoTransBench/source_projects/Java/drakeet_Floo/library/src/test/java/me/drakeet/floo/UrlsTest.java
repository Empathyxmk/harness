package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class UrlsTest {

    @Test
    public void testIsRemoteUrl() {
        assertTrue(Urls.isRemoteUrl("http://example.com"));
        assertTrue(Urls.isRemoteUrl("https://secure.com"));
        assertFalse(Urls.isRemoteUrl("file://local.txt"));
        assertFalse(Urls.isRemoteUrl("content://file"));
        assertFalse(Urls.isRemoteUrl(null));
        assertFalse(Urls.isRemoteUrl(""));
    }

    @Test
    public void testIsLocalUrl() {
        assertTrue(Urls.isLocalUrl("file://localfile.txt"));
        assertTrue(Urls.isLocalUrl("content://local"));
        assertFalse(Urls.isLocalUrl("http://remote.net"));
        assertFalse(Urls.isLocalUrl("https://secure.com"));
        assertFalse(Urls.isLocalUrl(null));
        assertFalse(Urls.isLocalUrl(""));
    }
}