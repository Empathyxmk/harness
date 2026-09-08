package com.yun.flogger.test.publics;

import com.cyfonly.flogger.utils.CommUtil;
import org.junit.Test;

import static org.junit.Assert.*;

public class CommUtilPublicTest {

    @Test
    public void testGetConfigByString_Public() {
        // Existing probably asserts default config values, use different default and key
        String val = CommUtil.getConfigByString("NONEXIST_PUBLIC_KEY", "DifferentDefaultPublic");
        assertEquals("DifferentDefaultPublic", val);
    }

    @Test
    public void testGetConfigByBoolean_Public() {
        // Key is almost certainly not present; flip the default compared to original tests
        boolean b1 = CommUtil.getConfigByBoolean("NONEXIST_PUBLIC_BOOL", true);
        assertTrue(b1);
        boolean b2 = CommUtil.getConfigByBoolean("NONEXIST_PUBLIC_BOOL", false);
        assertFalse(b2);
    }

    @Test
    public void testGetExpStack_Public() {
        Exception e = new IllegalArgumentException("PublicStackTrace");
        String stack = CommUtil.getExpStack(e);
        assertTrue(stack.contains("java.lang.IllegalArgumentException"));
        assertTrue(stack.contains("PublicStackTrace"));
    }
}