package com.example.colorama.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translation of colorama/tests/isatty_test.py (is_a_tty behaviors)
 */
public class IsattyTest {

    static class TTY { boolean isatty() { return true; }}
    static class NonTTY { boolean isatty() { return false; }}

    static boolean is_a_tty(Object stream) {
        if (stream instanceof TTY) return ((TTY) stream).isatty();
        if (stream instanceof NonTTY) return ((NonTTY) stream).isatty();
        return false;
    }

    @Test
    void test_TTY() {
        TTY tty = new TTY();
        assertTrue(is_a_tty(tty));
    }

    @Test
    void test_nonTTY() {
        NonTTY non_tty = new NonTTY();
        assertFalse(is_a_tty(non_tty));
    }

    @Test
    void test_withPycharm() {
        // Assume sys.stderr/stdout is always TTY for Java demonstration
        assertTrue(is_a_tty(new TTY()));
        assertTrue(is_a_tty(new TTY()));
    }

    @Test
    void test_withPycharmTTYOverride() {
        TTY tty = new TTY();
        assertTrue(is_a_tty(tty));
    }

    @Test
    void test_withPycharmNonTTYOverride() {
        NonTTY non_tty = new NonTTY();
        assertFalse(is_a_tty(non_tty));
    }

    @Test
    void test_withPycharmNoneOverride() {
        assertFalse(is_a_tty(null));
        assertFalse(is_a_tty(new NonTTY()));
        assertTrue(is_a_tty(new TTY()));
    }

    @Test
    void test_withPycharmStreamWrapped() {
        assertTrue(new TTY().isatty());
        assertFalse(new NonTTY().isatty());
    }
}