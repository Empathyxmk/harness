package com.asciimoo.drawille.original;

import com.asciimoo.drawille.*;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;


class ExtraTest {

    @Test
    void testGetTerminalSizeEnv() {
        // Set env variables for test
        Map<String, String> env = System.getenv();
        // Unfortunately, Java cannot set env variables at runtime in JDK API.
        // So we only check fallback logic
        int[] wh = ExtraUtil.getTerminalSize();
        assertTrue(wh[0] > 0);
        assertTrue(wh[1] > 0);
    }

    @Test
    void testNormalizeTypes() {
        assertEquals(5, ExtraUtil.normalize(5));
        assertEquals(5, ExtraUtil.normalize(4.7));
        assertThrows(IllegalArgumentException.class, () -> ExtraUtil.normalize("a"));
    }

    @Test
    void testIntDefaultDict() {
        Map<Object, Integer> d = ExtraUtil.intdefaultdict();
        assertNotNull(d);
        assertEquals(0, (int)d.get("x"));
    }

    @Test
    void testGetPos() {
        int[] r = ExtraUtil.get_pos(4, 8);
        assertEquals(2, r[0]);
        assertEquals(2, r[1]);
        // test w/ double
        r = ExtraUtil.get_pos(1.4, 3.6);
        assertEquals(0, r[0]);
        assertEquals(0, r[1]);
    }

    @Test
    void testCanvasUnsetUnknownType() {
        Canvas c = new Canvas();
        c.set(0, 0);
        c.chars.get(0).put(0, "test");
        c.unset(0, 0);
        // Should delete key, row may be removed.
    }

    @Test
    void testCanvasSetInvalidType() {
        Canvas c = new Canvas();
        c.chars.computeIfAbsent(0, k->new java.util.HashMap<>()).put(0, "str");
        c.set(0, 0);
        // Should not throw
    }

    @Test
    void testCanvasToggleCrossType() {
        Canvas c = new Canvas();
        c.chars.computeIfAbsent(0, k->new java.util.HashMap<>()).put(0, "xx");
        c.toggle(0, 0);
        // Should not throw
    }

    @Test
    void testCanvasLineEndingProperty() {
        Canvas c = new Canvas("END");
        assertEquals("END", c.lineEnding);
    }
}