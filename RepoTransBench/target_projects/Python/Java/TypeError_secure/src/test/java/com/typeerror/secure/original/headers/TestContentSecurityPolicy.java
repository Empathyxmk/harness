package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.ContentSecurityPolicy;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestContentSecurityPolicy {

    @Test
    public void testDefaultCsp() {
        ContentSecurityPolicy csp = new ContentSecurityPolicy();
        assertEquals(
            "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
            csp.getHeaderValue()
        );
    }

    @Test
    public void testCustomPolicy() {
        ContentSecurityPolicy csp =
            new ContentSecurityPolicy()
                .defaultSrc("'self'")
                .imgSrc("'self'", "cdn.example.com");
        assertEquals(
            "default-src 'self'; img-src 'self' cdn.example.com",
            csp.getHeaderValue()
        );
    }

    @Test
    public void testAddScriptSrc() {
        ContentSecurityPolicy csp = new ContentSecurityPolicy().scriptSrc("'self'", "'unsafe-inline'");
        assertTrue(csp.getHeaderValue().contains("script-src 'self' 'unsafe-inline'"));
    }

    @Test
    public void testClearPolicy() {
        ContentSecurityPolicy csp = new ContentSecurityPolicy().defaultSrc("'self'").clear();
        assertEquals(
            "default-src 'self'; script-src 'self'; style-src 'self'; object-src 'none'",
            csp.getHeaderValue()
        );
    }
}