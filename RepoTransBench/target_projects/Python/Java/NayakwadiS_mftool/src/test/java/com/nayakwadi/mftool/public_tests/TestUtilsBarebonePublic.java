package com.nayakwadi.mftool.public_tests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestUtilsBarebonePublic {
    @Test
    void test_basic_math_public() {
        assertEquals(2 * 3, 6);
        assertTrue(new java.util.HashMap<>() instanceof java.util.Map);
    }
}