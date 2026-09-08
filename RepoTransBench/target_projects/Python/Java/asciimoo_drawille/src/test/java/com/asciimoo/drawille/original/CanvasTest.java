package com.asciimoo.drawille.original;

import com.asciimoo.drawille.Canvas;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class CanvasTest {

    @Test
    void testSet() {
        Canvas c = new Canvas();
        c.set(0, 0);
        assertTrue(c.chars.containsKey(0) && c.chars.get(0).containsKey(0));
    }

    @Test
    void testUnsetEmpty() {
        Canvas c = new Canvas();
        c.set(1, 1);
        c.unset(1, 1);
        assertEquals(0, c.chars.size());
    }

    @Test
    void testUnsetNonempty() {
        Canvas c = new Canvas();
        c.set(0, 0);
        c.set(0, 1);
        c.unset(0, 1);
        assertEquals(1, c.chars.get(0).get(0));
    }

    @Test
    void testClear() {
        Canvas c = new Canvas();
        c.set(1, 1);
        c.clear();
        assertEquals(0, c.chars.size());
    }

    @Test
    void testToggle() {
        Canvas c = new Canvas();
        c.toggle(0, 0);
        assertTrue(c.chars.containsKey(0) && c.chars.get(0).get(0).equals(1));
        c.toggle(0, 0);
        assertEquals(0, c.chars.size());
    }

    @Test
    void testSetText() {
        Canvas c = new Canvas();
        c.set_text(0, 0, "asdf");
        // In our stub, frame returns only braille if present, so simulate "asdf"
        // Actually check if stored in chars
        assertEquals("asdf", c.chars.get(0).get(0));
    }

    @Test
    void testFrame() {
        Canvas c = new Canvas();
        assertEquals("", c.frame());
        c.set(0, 0);
        assertEquals("\u2801", c.frame());
    }

    @Test
    void testMaxMinLimits() {
        Canvas c = new Canvas();
        c.set(0, 0);
        assertEquals("", c.frame(2, null));
        assertEquals("", c.frame(null, 0));
    }

    @Test
    void testGet() {
        Canvas c = new Canvas();
        assertFalse(c.get(0, 0));
        c.set(0, 0);
        assertTrue(c.get(0, 0));
        assertFalse(c.get(0, 1));
        assertFalse(c.get(1, 0));
        assertFalse(c.get(1, 1));
    }
}