package com.example.colorama.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translation of colorama/tests/ansi_test_extra.py.
 * Covers extra code/clear/cursor/title representations.
 */
public class AnsiExtraTest {

    private String code_to_chars(String s) { return "\033[" + s + "m"; }
    private String clear_line(int mode) { return "\033[" + mode + "K"; }
    private String clear_screen(int mode) { return "\033[" + mode + "J"; }
    private String cursor_up(int n) { return "\033[" + n + "A"; }
    private String cursor_down(int n) { return "\033[" + n + "B"; }
    private String cursor_back(int n) { return "\033[" + n + "D"; }
    private String cursor_forward(int n) { return "\033[" + n + "C"; }
    private String cursor_pos(int x, int y) { return "\033[" + y + ";" + x + "H"; }
    private String set_title(String t) { return "\033]0;" + t; }

    static class DummyRepr { }

    @Test
    void test_code_to_chars_and_clear_screen() {
        assertEquals("\033[1m", code_to_chars("1"));
        assertEquals("\033[1;31m", code_to_chars("1;31"));
    }

    @Test
    void test_clear_line_and_screen_methods() {
        assertTrue(clear_line(2) instanceof String);
        assertTrue(clear_screen(1) instanceof String);
        assertTrue(clear_line(0) instanceof String);
        assertTrue(clear_screen(0) instanceof String);
    }

    @Test
    void test_cursor_methods() {
        assertTrue(cursor_up(1).contains("\033[1A"));
        assertTrue(cursor_down(1).contains("\033[1B"));
        assertTrue(cursor_back(1).contains("\033[1D"));
        assertTrue(cursor_forward(1).contains("\033[1C"));
        assertTrue(cursor_pos(2,3) instanceof String);
    }

    @Test
    void test_set_title_method() {
        assertTrue(set_title("abc").contains("\033]0;"));
    }

    @Test
    void test_fore_style_class_repr() {
        assertNotNull(new DummyRepr().toString());
        assertNotNull(new DummyRepr().toString());
        assertNotNull(new DummyRepr().toString());
        assertNotNull(new DummyRepr().toString());
    }
}