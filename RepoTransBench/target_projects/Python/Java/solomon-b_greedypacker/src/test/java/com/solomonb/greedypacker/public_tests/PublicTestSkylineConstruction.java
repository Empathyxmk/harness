package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestSkylineConstruction {
    Class<?> skylineClazz;
    Class<?> itemClazz;
    Object skyline;

    @BeforeEach
    void setUp() throws Exception {
        skylineClazz = Class.forName("com.solomonb.greedypacker.skyline.Skyline");
        itemClazz = Class.forName("com.solomonb.greedypacker.item.Item");
        skyline = skylineClazz.getConstructor(int.class, int.class, String.class).newInstance(8, 8, "bottom_left");
    }

    @Test
    void testInsertItems() throws Exception {
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(4, 6);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(4, 2);
        java.lang.reflect.Method insert = skylineClazz.getMethod("insert", itemClazz);
        insert.invoke(skyline, i1);
        insert.invoke(skyline, i2);

        int x1 = itemClazz.getField("x").getInt(i1);
        int y1 = itemClazz.getField("y").getInt(i1);
        int x2 = itemClazz.getField("x").getInt(i2);
        int y2 = itemClazz.getField("y").getInt(i2);
        assertTrue(x1 >= 0 && y1 >= 0);
        assertTrue(x2 >= 0 && y2 >= 0);
    }

    @Test
    void testOverflow() throws Exception {
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(8, 8);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(8, 8);
        skylineClazz.getMethod("insert", itemClazz).invoke(skyline, i1);
        Object insertResult = skylineClazz.getMethod("insert", itemClazz).invoke(skyline, i2);
        assertEquals(Boolean.FALSE, insertResult);
    }

    @Test
    void testReset() throws Exception {
        Object i = itemClazz.getConstructor(int.class, int.class).newInstance(5, 5);
        skylineClazz.getMethod("insert", itemClazz).invoke(skyline, i);
        skylineClazz.getMethod("reset").invoke(skyline);
        java.util.List<?> items = (java.util.List<?>) skylineClazz.getField("items").get(skyline);
        assertEquals(0, items.size());
    }
}