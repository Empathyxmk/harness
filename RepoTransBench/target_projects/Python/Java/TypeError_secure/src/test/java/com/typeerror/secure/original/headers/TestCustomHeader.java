package com.typeerror.secure.original.headers;

import com.typeerror.secure.headers.CustomHeader;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestCustomHeader {

    @Test
    public void testCustomHeaderInitAndProperties() {
        CustomHeader ch = new CustomHeader("X-Sample-Header", "init-value");
        assertEquals("X-Sample-Header", ch.getHeaderName());
        assertEquals("init-value", ch.getHeaderValue());
    }

    @Test
    public void testCustomHeaderSetChainAndOverride() {
        CustomHeader ch = new CustomHeader("X-Chain", "val1");
        CustomHeader ret = ch.set("val2");
        assertEquals("val2", ch.getHeaderValue());
        assertSame(ch, ret);
    }

    @Test
    public void testCustomHeaderSetEdgeCases() {
        CustomHeader ch = new CustomHeader("X-Edge", "start");
        ch.set("");
        assertEquals("", ch.getHeaderValue());
        ch.set("123");
        assertEquals("123", ch.getHeaderValue());
    }
}