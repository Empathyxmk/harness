package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestCache {

    @Test
    void testDefaultBackend() {
        CacheConfig config = CacheConfig.defaultCache();
        assertEquals("locmem", config.getBackend());
        assertEquals("default", config.getLocation());
    }

    @Test
    void testCustomBackend() {
        CacheConfig config = new CacheConfig("redis", "redis:6379");
        assertEquals("redis", config.getBackend());
        assertEquals("redis:6379", config.getLocation());
    }
}