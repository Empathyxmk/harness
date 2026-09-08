package com.zqqqqz2000.shshsh.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class GlobalVarsTest {
    static String GLOBAL_VALUE;

    @Test
    void testSetAndGetGlobalValue() {
        GLOBAL_VALUE = "Hello";
        assertEquals("Hello", GLOBAL_VALUE);
        GLOBAL_VALUE = "World";
        assertEquals("World", GLOBAL_VALUE);
    }

    @Test
    void testGlobalValueIsNullAtStart() {
        GLOBAL_VALUE = null;
        assertNull(GLOBAL_VALUE);
    }
}