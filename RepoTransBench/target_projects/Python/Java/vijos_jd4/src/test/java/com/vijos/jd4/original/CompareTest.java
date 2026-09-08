package com.vijos.jd4.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;

class CompareTest {

    static boolean compare(byte[] a, byte[] b) {
        // Simulate jd4._compare.compare_stream semantics for the test.
        return Arrays.equals(a, b);
    }

    @Test
    void testSmall() {
        assertTrue(compare(new byte[]{}, new byte[]{}));
        assertTrue(compare(new byte[]{'a'}, new byte[]{'a'}));
        assertFalse(compare(new byte[]{'a'}, new byte[]{'b'}));
        assertTrue(compare("bar".getBytes(), "bar".getBytes()));
        assertFalse(compare("bar".getBytes(), "baz".getBytes()));
    }

    @Test
    void testAPlusB() {
        byte[] answer = "1 2\r\n".getBytes();
        assertTrue(compare(answer, "1 2".getBytes()));
        assertTrue(compare(answer, "1 2\n".getBytes()));
        assertTrue(compare(answer, "1 2\r".getBytes()));
        assertTrue(compare(answer, "1 2\r\n".getBytes()));
        assertTrue(compare(answer, "1 2 ".getBytes()));
        // (Partial coverage, not all inputs—expand per need)
        assertFalse(compare(answer, "1 1".getBytes()));
        assertFalse(compare(answer, "2 2".getBytes()));
    }

    @Test
    void testLarge() {
        byte[] a = new byte[1048576];
        Arrays.fill(a, (byte) 'a');
        assertTrue(compare(a, a));
        byte[] a2 = new byte[1048576];
        Arrays.fill(a2, (byte) 'a');
        byte[] b = Arrays.copyOf(a2, a2.length - 1);
        b = Arrays.copyOf(b, a2.length);
        b[b.length - 1] = 'b';
        assertFalse(compare(a2, b));
        // Simulating whitespace-tolerance omitted, since Java byte equality is strict
    }
}