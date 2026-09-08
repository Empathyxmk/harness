package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestMaximalRectangles {

    Object mx;
    Class<?> itemClazz;

    @BeforeEach
    void setUp() throws Exception {
        Class<?> mxClazz = Class.forName("com.solomonb.greedypacker.maximal_rectangles.MaximalRectangles");
        mx = mxClazz.getConstructor(int.class, int.class, String.class).newInstance(30, 18, "contact_point");
        itemClazz = Class.forName("com.solomonb.greedypacker.Item");
    }

    @Test
    void testInserts() throws Exception {
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(5, 5);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(6, 3);
        Object i3 = itemClazz.getConstructor(int.class, int.class).newInstance(3, 7);

        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i1);
        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i2);
        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i3);

        int x1 = itemClazz.getField("x").getInt(i1);
        int y1 = itemClazz.getField("y").getInt(i1);
        int x2 = itemClazz.getField("x").getInt(i2);
        int y2 = itemClazz.getField("y").getInt(i2);
        int x3 = itemClazz.getField("x").getInt(i3);
        int y3 = itemClazz.getField("y").getInt(i3);

        assertTrue(x1 >= 0 && y1 >= 0);
        assertTrue(x2 >= 0 && y2 >= 0);
        assertTrue(x3 >= 0 && y3 >= 0);
    }

    @Test
    void testReset() throws Exception {
        Object i = itemClazz.getConstructor(int.class, int.class).newInstance(4, 4);
        mx.getClass().getMethod("insert", itemClazz).invoke(mx, i);
        mx.getClass().getMethod("reset").invoke(mx);
        @SuppressWarnings("unchecked")
        java.util.List<Object> items = (java.util.List<Object>) mx.getClass().getField("items").get(mx);
        assertEquals(0, items.size());
    }
}