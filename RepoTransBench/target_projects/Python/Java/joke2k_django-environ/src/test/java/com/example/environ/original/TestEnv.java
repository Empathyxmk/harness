package com.example.environ.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;
import java.util.LinkedHashMap;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from: tests/test_env.py
 * This assumes Env class implements similar functionality as the python environ.Env.
 */
public class TestEnv {

    private Env env;

    @BeforeEach
    void setUp() {
        // Simulate environment with some defaults
        Map<String, String> envMap = new LinkedHashMap<>();
        envMap.put("DEBUG", "True");
        envMap.put("PORT", "8000");
        envMap.put("INTVAR", "123");
        envMap.put("FLOATVAR", "12.34");
        env = new Env(envMap);
    }

    @Test
    void testStrCast() {
        String v = env.get("DEBUG");
        assertEquals("True", v);
    }

    @Test
    void testIntCast() {
        int port = env.getInt("PORT");
        assertEquals(8000, port);
    }

    @Test
    void testIntParsing() {
        int intval = env.getInt("INTVAR");
        assertEquals(123, intval);
    }

    @Test
    void testFloatParsing() {
        float floatval = env.getFloat("FLOATVAR");
        assertEquals(12.34f, floatval, 0.0001f);
    }

    @Test
    void testGetUnknownIsNull() {
        assertNull(env.get("DOES_NOT_EXIST"));
    }

    @Test
    void testDefaultFallback() {
        assertEquals("fallback", env.get("NOT_SET", "fallback"));
    }
}