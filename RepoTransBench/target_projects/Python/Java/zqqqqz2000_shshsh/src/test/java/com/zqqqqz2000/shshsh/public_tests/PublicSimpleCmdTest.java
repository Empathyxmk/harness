package com.zqqqqz2000.shshsh.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSimpleCmdTest {
    String simpleUpper(String s) {
        return s.toUpperCase();
    }

    String simpleReverse(String s) {
        return new StringBuilder(s).reverse().toString();
    }

    @Test
    void testSimpleUpper() {
        assertEquals("HELLO", simpleUpper("hello"));
    }

    @Test
    void testSimpleReverse() {
        assertEquals("olleh", simpleReverse("hello"));
    }
}