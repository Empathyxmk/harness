package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestMaximalRectanglesConstructor {

    @Test
    void testInitAndRepr() throws Exception {
        Class<?> mrClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        Object mr = mrClazz.getConstructor(int.class, int.class, String.class).newInstance(8, 8, "area_fit");
        assertEquals(8, mrClazz.getField("width").getInt(mr));
        assertEquals(8, mrClazz.getField("height").getInt(mr));
        assertTrue(mr.toString().contains("MaximalRectangles"));
    }

    @Test
    void testInvalidHeuristic() throws Exception {
        Class<?> mrClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        Exception ex = assertThrows(Exception.class, () -> {
            mrClazz.getConstructor(int.class, int.class, String.class).newInstance(8, 8, "unknown");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"));
    }
}