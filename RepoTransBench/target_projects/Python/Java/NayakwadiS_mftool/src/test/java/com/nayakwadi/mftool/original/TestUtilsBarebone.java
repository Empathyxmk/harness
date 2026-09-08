package com.nayakwadi.mftool.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class TestUtilsBarebone {
    @Test
    void test_basic_math() {
        assertEquals(1 + 1, 2);
        assertTrue(new java.util.ArrayList<>() instanceof java.util.List);
    }
}