package com.facebook.sparts.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

import java.util.HashMap;
import java.util.Map;

public class SetTaskOptionTest {
    @Test
    public void testBasicSetting() {
        Map<String, String> opts = new HashMap<>();
        opts.put("foo", "bar");
        assertEquals("bar", opts.get("foo"));
        opts.put("foo", "baz");
        assertEquals("baz", opts.get("foo"));
    }
}