package com.yun.flogger.test;

import com.cyfonly.flogger.utils.CommUtil;
import org.junit.Test;

import static org.junit.Assert.*;

public class CommUtilTest {

    @Test
    public void testGetConfigByStringAndInt() {
        // fallback to default
        assertEquals("fallback", CommUtil.getConfigByString("NOSUCHKEY", "fallback"));
        assertEquals(123, CommUtil.getConfigByInt("NOSUCHINT", 123));
    }

    @Test
    public void testGetConfigByLong() {
        long val = CommUtil.getConfigByLong("NOSUCHLONG", 100L);
        assertEquals(100L, val);
    }

    @Test
    public void testGetConfigByBoolean() {
        assertTrue(CommUtil.getConfigByBoolean("NOSUCHBOOL", true));
        assertFalse(CommUtil.getConfigByBoolean("NOSUCHBOOL", false));
    }

    @Test
    public void testStringToBytes() {
        String s = "abc123";
        byte[] b = CommUtil.StringToBytes(s);
        assertArrayEquals(s.getBytes(), b);
    }

    @Test
    public void testGetExpStack() {
        Exception e = new Exception("expected");
        String stack = CommUtil.getExpStack(e);
        assertTrue(stack.contains("expected"));
    }
}