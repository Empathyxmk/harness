package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestSkylineConstructor {

    @Test
    void testSkylineConstructors() throws Exception {
        Class<?> skylineClazz = Class.forName("com.solomonb.greedypacker.skyline.Skyline");
        Object skyline = skylineClazz.getConstructor(int.class, int.class, String.class)
                .newInstance(9, 5, "bottom_left");
        assertEquals(9, skylineClazz.getField("width").getInt(skyline));
        assertEquals(5, skylineClazz.getField("height").getInt(skyline));
    }

    @Test
    void testInvalidHeuristic() throws Exception {
        Class<?> skylineClazz = Class.forName("com.solomonb.greedypacker.skyline.Skyline");
        Exception ex = assertThrows(Exception.class, () -> {
            skylineClazz.getConstructor(int.class, int.class, String.class)
                    .newInstance(9, 5, "notarealheuristic");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"));
    }
}