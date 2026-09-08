package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.ReferrerPolicy;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestReferrerPolicy {

    @Test
    public void testDefaultReferrerPolicy() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy();
        assertEquals("strict-origin-when-cross-origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testSetCustomPolicy() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().set("no-referrer");
        assertEquals("no-referrer", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testNoReferrer() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().noReferrer();
        assertEquals("no-referrer", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testNoReferrerWhenDowngrade() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().noReferrerWhenDowngrade();
        assertEquals("no-referrer-when-downgrade", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testOrigin() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().origin();
        assertEquals("origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testOriginWhenCrossOrigin() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().originWhenCrossOrigin();
        assertEquals("origin-when-cross-origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testSameOrigin() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().sameOrigin();
        assertEquals("same-origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testStrictOrigin() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().strictOrigin();
        assertEquals("strict-origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testStrictOriginWhenCrossOrigin() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().strictOriginWhenCrossOrigin();
        assertEquals("strict-origin-when-cross-origin", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testUnsafeUrl() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().unsafeUrl();
        assertEquals("unsafe-url", referrerPolicy.getHeaderValue());
    }

    @Test
    public void testClearPolicy() {
        ReferrerPolicy referrerPolicy = new ReferrerPolicy().set("custom-policy").clear();
        assertEquals("strict-origin-when-cross-origin", referrerPolicy.getHeaderValue());
    }
}