package com.example.flaskbabel.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSpeakLaterTest {

    String f(int a, int b) { return "val(" + a + "," + b + ")"; }

    @Test
    void testPublicStrAndRepr() {
        LazyString lz = new LazyString(() -> f(2, 5));
        assertEquals("val(2,5)", lz.toString());
        assertEquals("l'val(2,5)'", lz.repr());
    }

    @Test
    void testPublicLenGetItemIterContains() {
        LazyString lz = new LazyString(() -> "hello Java");
        assertEquals(10, lz.length());
        assertEquals('h', lz.charAt(0));
        assertEquals("ello", lz.substring(1, 5));
        StringBuilder sb = new StringBuilder();
        for (char c : lz.toString().toCharArray()) sb.append(c);
        assertEquals("hello Java", sb.toString());
        assertTrue(lz.toString().contains("Java"));
        assertFalse(lz.toString().contains("xyz"));
    }

    @Test
    void testPublicAddRadd() {
        LazyString lz = new LazyString(() -> "foo");
        assertEquals("foobar", lz.plus("bar"));
        assertEquals("barfoo", lz.rplus("bar"));
    }
}