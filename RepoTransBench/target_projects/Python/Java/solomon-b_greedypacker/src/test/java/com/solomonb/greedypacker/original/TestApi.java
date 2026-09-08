package com.solomonb.greedypacker.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestApi {

    @Test
    void testBinManagerAndItem() throws Exception {
        // Simulates: bm = greedypacker.BinManager(15, 12)
        Class<?> binManagerClazz = Class.forName("com.solomonb.greedypacker.BinManager");
        Object bm = binManagerClazz.getConstructor(int.class, int.class).newInstance(15, 12);
        Class<?> itemClazz = Class.forName("com.solomonb.greedypacker.Item");
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(7, 3);

        // bm.insert(i1)
        int binIndex = (int)binManagerClazz.getMethod("insert", itemClazz).invoke(bm, i1);
        assertEquals(0, binIndex);
        Object bin0 = ((java.util.List<?>)binManagerClazz.getField("bins").get(bm)).get(0);
        int binWidth = bin0.getClass().getField("width").getInt(bin0);
        int binHeight = bin0.getClass().getField("height").getInt(bin0);
        int i1Width = itemClazz.getField("width").getInt(i1);
        int i1Height = itemClazz.getField("height").getInt(i1);

        assertTrue(binWidth >= i1Width);
        assertTrue(binHeight >= i1Height);

        assertEquals(Integer.TYPE, itemClazz.getField("x").getType());
        assertEquals(Integer.TYPE, itemClazz.getField("y").getType());

        assertTrue(binManagerClazz.getMethod("insert", itemClazz).canAccess(bm));
    }
}