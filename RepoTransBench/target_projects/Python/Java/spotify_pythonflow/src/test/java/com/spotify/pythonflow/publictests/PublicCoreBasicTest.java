package com.spotify.pythonflow.publictests;

import org.junit.jupiter.api.Test;

import java.util.HashMap;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class PublicCoreBasicTest {

    // Note: In real test, would use the main Graph/Operation classes from prod
    static class DummyOp {
        int field;
        DummyOp(int f) { this.field = f; }
    }

    @Test
    public void testPublicGraphContextMap() {
        // Just a simple public test for mapping logic
        Map<String, Integer> ctx = new HashMap<>();
        ctx.put("foo", 1);
        ctx.put("bar", 2);
        assertEquals(2, ctx.size());
        assertTrue(ctx.containsKey("foo"));
        assertTrue(ctx.containsKey("bar"));
        assertEquals(1, ctx.get("foo"));
        assertEquals(2, ctx.get("bar"));
    }
}