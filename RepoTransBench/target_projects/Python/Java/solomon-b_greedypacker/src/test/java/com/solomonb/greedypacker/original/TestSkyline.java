package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestSkyline {

    @Test
    void testHeuristics() {
        try {
            Object sk = Class.forName("com.solomonb.greedypacker.skyline.Skyline")
                .getConstructor(int.class, int.class, String.class)
                .newInstance(6, 3, "best_fit");
            assertEquals(6, sk.getClass().getField("width").getInt(sk));
            sk = Class.forName("com.solomonb.greedypacker.skyline.Skyline")
                    .getConstructor(int.class, int.class, String.class)
                    .newInstance(6, 3, "bottom_left");
            assertEquals(3, sk.getClass().getField("height").getInt(sk));
        } catch (NoSuchFieldException | IllegalAccessException e) {
            fail("Fields missing: " + e.getMessage());
        } catch (Exception e) {
            fail("Constructor or instantiation failed: " + e.getMessage());
        }

        Exception ex = assertThrows(Exception.class, () -> {
            Class.forName("com.solomonb.greedypacker.skyline.Skyline")
                    .getConstructor(int.class, int.class, String.class)
                    .newInstance(6, 3, "unknown_heuristic");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"));
    }

    @Test
    void testRepr() throws Exception {
        Object sk = Class.forName("com.solomonb.greedypacker.skyline.Skyline")
                .getConstructor(int.class, int.class)
                .newInstance(3, 3);
        assertTrue(sk.toString().contains("Skyline"));
    }
}