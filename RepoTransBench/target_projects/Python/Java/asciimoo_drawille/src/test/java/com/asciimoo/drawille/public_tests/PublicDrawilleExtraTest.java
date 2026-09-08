package com.asciimoo.drawille.public_tests;

import com.asciimoo.drawille.*;
import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;

class PublicDrawilleExtraTest {

    @Test
    void testGetTerminalSizeEnvPublic() {
        // We cannot monkeypatch System.getenv, so just check method returns plausible
        int[] size = ExtraUtil.getTerminalSize();
        assertTrue(size[0] > 0);
        assertTrue(size[1] > 0);
    }

    @Test
    void testNormalizeTypesPublic() {
        assertEquals(15, ExtraUtil.normalize(15));
        assertEquals(18, ExtraUtil.normalize(17.8));
        assertThrows(IllegalArgumentException.class, () -> ExtraUtil.normalize(new int[]{}));
        assertThrows(IllegalArgumentException.class, () -> ExtraUtil.normalize("xyz"));
    }

    @Test
    void testIntDefaultDictPublic() {
        Map<Object, Integer> d = ExtraUtil.intdefaultdict();
        assertNotNull(d);
        assertEquals(0, (int)d.get(222));
        d.put(222, d.get(222) + 55);
        assertEquals(55, (int)d.get(222));
    }

    @Test
    void testGetPosPublic() {
        int[] got = ExtraUtil.get_pos(7, 9);
        assertEquals(3, got[0]);
        assertEquals(2, got[1]);
        got = ExtraUtil.get_pos(4.9, 15.2);
        assertEquals(2, got[0]);
        assertEquals(3, got[1]);
    }

    @Test
    void testCanvasUnsetUnknownTypePublic() {
        Canvas c = new Canvas();
        c.set(4, 10);
        c.chars.computeIfAbsent(4, k->new java.util.HashMap<>()).put(10, new int[]{15, 30});
        c.unset(4, 10);
    }

    @Test
    void testCanvasSetInvalidTypePublic() {
        Canvas c = new Canvas();
        c.chars.computeIfAbsent(6, k->new java.util.HashMap<>()).put(7, 9.81);
        c.set(6, 7);
    }

    @Test
    void testCanvasToggleCrossTypePublic() {
        Canvas c = new Canvas();
        c.chars.computeIfAbsent(9, k->new java.util.HashMap<>()).put(12, null);
        c.toggle(9, 12);
    }

    @Test
    void testCanvasLineEndingPropertyPublic() {
        Canvas c = new Canvas("LF");
        assertEquals("LF", c.lineEnding);
    }
}