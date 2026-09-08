package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestShelf {

    private Object shelf;
    private Class<?> shelfClazz;
    private Class<?> itemClazz;

    @BeforeEach
    void setUp() throws Exception {
        shelfClazz = Class.forName("com.solomonb.greedypacker.shelf.Shelf");
        itemClazz = Class.forName("com.solomonb.greedypacker.item.Item");
        shelf = shelfClazz.getConstructor(int.class, int.class, String.class).newInstance(12, 8, "next_fit");
    }

    @AfterEach
    void tearDown() {
        shelf = null;
    }

    @Test
    void testInsertSingle() throws Exception {
        Object I = itemClazz.getConstructor(int.class, int.class).newInstance(4, 4);
        shelfClazz.getMethod("insert", itemClazz).invoke(shelf, I);

        int x = itemClazz.getField("x").getInt(I);
        int y = itemClazz.getField("y").getInt(I);

        assertEquals(0, x, "Expected inserted item x=0");
        assertEquals(0, y, "Expected inserted item y=0");
    }

    @Test
    void testInsertMulti() throws Exception {
        Object I0 = itemClazz.getConstructor(int.class, int.class).newInstance(3, 2);
        Object I1 = itemClazz.getConstructor(int.class, int.class).newInstance(2, 2);
        Object I2 = itemClazz.getConstructor(int.class, int.class).newInstance(5, 3);
        Object I3 = itemClazz.getConstructor(int.class, int.class).newInstance(1, 1);

        Object[] objs = {I0, I1, I2, I3};
        for (Object obj : objs) {
            shelfClazz.getMethod("insert", itemClazz).invoke(shelf, obj);
        }

        java.util.List<?> shelves = (java.util.List<?>) shelfClazz.getField("shelves").get(shelf);
        Object firstShelf = shelves.get(0);
        int width = firstShelf.getClass().getField("width").getInt(firstShelf);
        assertEquals(6, width);
        assertEquals(2, shelves.size());
    }

    @Test
    void testHeightLimit() throws Exception {
        Object I0 = itemClazz.getConstructor(int.class, int.class).newInstance(10, 7);
        Object I1 = itemClazz.getConstructor(int.class, int.class).newInstance(12, 2);
        java.lang.reflect.Method insert = shelfClazz.getMethod("insert", itemClazz);
        insert.invoke(shelf, I0);

        java.util.List<?> shelvesList = (java.util.List<?>) shelfClazz.getField("shelves").get(shelf);
        Object firstShelf = shelvesList.get(0);
        int height = firstShelf.getClass().getField("height").getInt(firstShelf);
        assertEquals(7, height);

        Object res = insert.invoke(shelf, I1);
        assertEquals(Boolean.FALSE, res);
    }

    @Test
    void testRepr() throws Exception {
        assertTrue(shelf.toString().contains("Shelf"));
    }

    @Test
    void testInvalidHeuristic() throws Exception {
        Exception ex = assertThrows(Exception.class, () -> {
            shelfClazz.getConstructor(int.class, int.class, String.class).newInstance(5, 5, "nonexistent");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"));
    }
}