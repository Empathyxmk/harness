package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestGuillotine {

    @Test
    void testGuillotineInsert() throws Exception {
        Class<?> guillotineClazz = Class.forName("com.solomonb.greedypacker.guillotine.Guillotine");
        Class<?> itemClazz = Class.forName("com.solomonb.greedypacker.Item");

        Object guillotine = guillotineClazz.getConstructor(int.class, int.class, String.class)
                .newInstance(10, 10, "short_side");
        Object item = itemClazz.getConstructor(int.class, int.class).newInstance(5, 5);

        boolean result = (boolean) guillotineClazz.getMethod("insert", itemClazz).invoke(guillotine, item);

        assertTrue(result, "Guillotine should successfully insert an item that fits");

        int x = itemClazz.getField("x").getInt(item);
        int y = itemClazz.getField("y").getInt(item);

        assertTrue(x >= 0 && y >= 0, "Inserted item should have a valid position");
    }

    @Test
    void testGuillotineRejectsLargeItem() throws Exception {
        Class<?> guillotineClazz = Class.forName("com.solomonb.greedypacker.guillotine.Guillotine");
        Class<?> itemClazz = Class.forName("com.solomonb.greedypacker.Item");

        Object guillotine = guillotineClazz.getConstructor(int.class, int.class, String.class)
                .newInstance(8, 8, "short_side");
        Object item = itemClazz.getConstructor(int.class, int.class).newInstance(10, 9);

        boolean result = (boolean) guillotineClazz.getMethod("insert", itemClazz).invoke(guillotine, item);
        assertFalse(result, "Guillotine should reject an item that does not fit");
    }
}