package com.solomonb.greedypacker.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestApi {

    @Test
    void testBinManagerInsertAndBins() throws Exception {
        Class<?> binManagerClazz = Class.forName("com.solomonb.greedypacker.BinManager");
        Class<?> itemClazz = Class.forName("com.solomonb.greedypacker.Item");
        Object bm = binManagerClazz.getConstructor(int.class, int.class).newInstance(6, 6);
        Object i1 = itemClazz.getConstructor(int.class, int.class).newInstance(4, 2);
        Object i2 = itemClazz.getConstructor(int.class, int.class).newInstance(5, 3);
        Object i3 = itemClazz.getConstructor(int.class, int.class).newInstance(7, 5);

        int binIndex1 = (int)binManagerClazz.getMethod("insert", itemClazz).invoke(bm, i1);
        int binIndex2 = (int)binManagerClazz.getMethod("insert", itemClazz).invoke(bm, i2);
        // i3 too large, expect -1 or similar indicator for failure
        Object result = binManagerClazz.getMethod("insert", itemClazz).invoke(bm, i3);
        assertTrue(result instanceof Integer, "Insert should return an int");
        int failedIndex = (Integer) result;
        assertEquals(-1, failedIndex, "Insert should fail for item too large to fit");

        // Ensure first two bins are correct
        java.util.List<?> bins = (java.util.List<?>) binManagerClazz.getField("bins").get(bm);
        assertTrue(bins.size() >= 1, "At least one bin allocated");
    }
}