package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.CrossOriginOpenerPolicy;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCrossOriginOpenerPolicy {

    @Test
    public void testDefaultCoop() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy();
        assertEquals("same-origin", coop.getHeaderValue());
    }

    @Test
    public void testSetCustomPolicy() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy().set("custom-policy");
        assertEquals("custom-policy", coop.getHeaderValue());
    }

    @Test
    public void testSameOrigin() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy().sameOrigin();
        assertEquals("same-origin", coop.getHeaderValue());
    }

    @Test
    public void testSameOriginAllowPopups() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy().sameOriginAllowPopups();
        assertEquals("same-origin-allow-popups", coop.getHeaderValue());
    }

    @Test
    public void testUnsafeNone() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy().unsafeNone();
        assertEquals("unsafe-none", coop.getHeaderValue());
    }

    @Test
    public void testClearPolicy() {
        CrossOriginOpenerPolicy coop = new CrossOriginOpenerPolicy().set("custom-policy").clear();
        assertEquals("same-origin", coop.getHeaderValue());
    }
}