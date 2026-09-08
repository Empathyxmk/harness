package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestGuillotine {

    private Object guillotine;
    private Class<?> itemClazz;

    @BeforeEach
    void setUp() throws Exception {
        // Equivalent to: self.G = Guillotine(14, 13, heuristic="short_side")
        Class<?> guillotineClazz = Class.forName("com.solomonb.greedypacker.guillotine.Guillotine");
        guillotine = guillotineClazz.getConstructor(int.class, int.class, String.class).newInstance(14, 13, "short_side");
        itemClazz = Class.forName("com.solomonb.greedypacker.Item");
    }

    @Test
    void testInsertAndCoordinates() throws Exception {
        Object I = itemClazz.getConstructor(int.class, int.class).newInstance(8, 4);
        boolean result = (boolean) guillotine.getClass().getMethod("insert", itemClazz).invoke(guillotine, I);
        assertTrue(result);
        int binWidth = guillotine.getClass().getField("width").getInt(guillotine);
        int binHeight = guillotine.getClass().getField("height").getInt(guillotine);
        int x = itemClazz.getField("x").getInt(I);
        int y = itemClazz.getField("y").getInt(I);
        int iWidth = itemClazz.getField("width").getInt(I);
        int iHeight = itemClazz.getField("height").getInt(I);
        assertTrue(binWidth >= x + iWidth);
        assertTrue(binHeight >= y + iHeight);
    }

    @Test
    void testInvalidHeuristic() throws Exception {
        Class<?> guillotineClazz = Class.forName("com.solomonb.greedypacker.guillotine.Guillotine");
        Exception ex = assertThrows(Exception.class, () -> {
            guillotineClazz.getConstructor(int.class, int.class, String.class).newInstance(4, 7, "nonsense");
        });
        assertTrue(ex.getCause().getMessage().toLowerCase().contains("value"));
    }
}