package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.XFrameOptions;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestXFrameOptions {

    @Test
    public void testXFrameOptionsDefaults() {
        XFrameOptions xfo = new XFrameOptions();
        assertEquals("SAMEORIGIN", xfo.getHeaderValue());
    }

    @Test
    public void testSetAndClearValue() {
        XFrameOptions xfo = new XFrameOptions();
        xfo.set("foo");
        assertEquals("foo", xfo.getHeaderValue());
        xfo.clear();
        assertEquals("SAMEORIGIN", xfo.getHeaderValue());
    }

    @Test
    public void testDenyAndSameoriginMethods() {
        XFrameOptions xfo = new XFrameOptions();
        xfo.deny();
        assertEquals("DENY", xfo.getHeaderValue());
        xfo.sameorigin();
        assertEquals("SAMEORIGIN", xfo.getHeaderValue());
    }
}