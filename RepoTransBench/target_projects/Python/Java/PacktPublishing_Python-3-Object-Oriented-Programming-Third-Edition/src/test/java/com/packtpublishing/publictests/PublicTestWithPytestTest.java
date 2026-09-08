package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestWithPytestTest {

    @Test
    void testTrue() {
        assertTrue(true);
    }

    @Test
    void testEquals() {
        assertEquals("abc", "a" + "b" + "c");
    }
}