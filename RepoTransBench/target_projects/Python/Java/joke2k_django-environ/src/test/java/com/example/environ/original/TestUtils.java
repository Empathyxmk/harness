package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestUtils {

    @Test
    void testStrToBool() {
        assertTrue(Utils.strToBool("1"));
        assertTrue(Utils.strToBool("True"));
        assertTrue(Utils.strToBool("yes"));
        assertFalse(Utils.strToBool("no"));
        assertFalse(Utils.strToBool("0"));
        assertFalse(Utils.strToBool("False"));
        assertFalse(Utils.strToBool(null));
    }

    @Test
    void testCastToInt() {
        assertEquals(12, Utils.castToInt("12"));
    }

    @Test
    void testCastToFloat() {
        assertEquals(3.14f, Utils.castToFloat("3.14"), 0.0001f);
    }

    @Test
    void testEnvVarFallback() {
        String result = Utils.readEnv("MISSING_VAR", "fallback");
        assertEquals("fallback", result);
    }
}