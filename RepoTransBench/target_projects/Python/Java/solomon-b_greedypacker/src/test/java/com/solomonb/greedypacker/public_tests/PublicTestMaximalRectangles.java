package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestMaximalRectangles {

    Object mx;
    Class<?> itemClazz;

    @BeforeEach
    void setUp() throws Exception {
        Class<?> mxClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        mx = mxClazz.getConstructor(int.class, int.class, String.class).newInstance(25, 15, "area_fit");
        itemClazz = Class.forName("com.solomonb.greedypacker.Item");
    }

    @Test
    void testInsertionAndPositions() throws Exception {
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(5, 4);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(4, 3);

        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i1);
        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i2);

        int x1 = itemClazz.getField("x").getInt(i1);
        int y1 = itemClazz.getField("y").getInt(i1);

        assertTrue(x1 >= 0 && y1 >= 0);

        int x2 = itemClazz.getField("x").getInt(i2);
        int y2 = itemClazz.getField("y").getInt(i2);

        assertTrue(x2 >= 0 && y2 >= 0);
    }

    @Test
    void testReset() throws Exception {
        Object i = itemClazz.getConstructor(int.class, int.class).newInstance(5, 5);
        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i);
        mx.getClass().getMethod("reset").invoke(mx);
        java.util.List<?> items = (java.util.List<?>) mx.getClass().getField("items").get(mx);
        assertEquals(0, items.size());
    }
}