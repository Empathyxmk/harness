package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.CacheControl;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCacheControl {

    @Test
    public void testDefaultCacheControl() {
        CacheControl control = new CacheControl();
        assertEquals("no-store", control.getHeaderValue());
    }

    @Test
    public void testSetNoCache() {
        CacheControl control = new CacheControl().noCache();
        assertTrue(control.getHeaderValue().contains("no-cache"));
    }

    @Test
    public void testSetMaxAge() {
        CacheControl control = new CacheControl().maxAge(3600);
        assertTrue(control.getHeaderValue().contains("max-age=3600"));
    }

    @Test
    public void testClearCacheControl() {
        CacheControl control = new CacheControl().noCache().clear();
        assertEquals("no-store", control.getHeaderValue());
    }

    @Test
    public void testMultipleDirectives() {
        CacheControl control = new CacheControl().noCache().mustRevalidate().maxAge(3600);
        assertEquals("no-cache, must-revalidate, max-age=3600", control.getHeaderValue());
    }
}