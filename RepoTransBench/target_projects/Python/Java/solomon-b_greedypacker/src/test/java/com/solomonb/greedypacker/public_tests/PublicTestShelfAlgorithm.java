package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestShelfAlgorithm {

    private Object shelf;
    private Class<?> shelfClazz;
    private Class<?> itemClazz;

    @BeforeEach
    void setUp() throws Exception {
        shelfClazz = Class.forName("com.solomonb.greedypacker.shelf.Shelf");
        itemClazz = Class.forName("com.solomonb.greedypacker.item.Item");
        shelf = shelfClazz.getConstructor(int.class, int.class, String.class).newInstance(10, 6, "next_fit");
    }

    @Test
    void testShelfInsert() throws Exception {
        Object item = itemClazz.getConstructor(int.class, int.class).newInstance(6, 5);
        shelfClazz.getMethod("insert", itemClazz).invoke(shelf, item);

        int x = itemClazz.getField("x").getInt(item);
        int y = itemClazz.getField("y").getInt(item);

        assertEquals(0, x, "Inserted item should be at x=0");
        assertEquals(0, y, "Inserted item should be at y=0");
    }

    @Test
    void testMultipleShelfInsert() throws Exception {
        Object i0 = itemClazz.getConstructor(int.class, int.class).newInstance(4, 3);
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(5, 3);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(3, 2);

        Object[] arr = {i0, i1, i2};
        for (Object obj : arr) {
            shelfClazz.getMethod("insert", itemClazz).invoke(shelf, obj);
        }

        java.util.List<?> shelvesList = (java.util.List<?>) shelfClazz.getField("shelves").get(shelf);
        assertTrue(shelvesList.size() >= 1);
    }

    @Test
    void testRepr() {
        assertTrue(shelf.toString().contains("Shelf"));
    }
}