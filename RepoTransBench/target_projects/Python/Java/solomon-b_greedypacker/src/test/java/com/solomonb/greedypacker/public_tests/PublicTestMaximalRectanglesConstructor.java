package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestMaximalRectanglesConstructor {

    @Test
    void testValidConstructor() throws Exception {
        Class<?> maxRectClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        Object maxRect = maxRectClazz.getConstructor(int.class, int.class, String.class).newInstance(7, 10, "contact_point");
        assertEquals(7, maxRectClazz.getField("width").getInt(maxRect));
        assertEquals(10, maxRectClazz.getField("height").getInt(maxRect));
    }

    @Test
    void testInvalidHeuristic() throws Exception {
        Class<?> maxRectClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        Exception ex = assertThrows(Exception.class, () -> {
            maxRectClazz.getConstructor(int.class, int.class, String.class).newInstance(3, 4, "madeup");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"), "Exception should mention invalid value");
    }
}