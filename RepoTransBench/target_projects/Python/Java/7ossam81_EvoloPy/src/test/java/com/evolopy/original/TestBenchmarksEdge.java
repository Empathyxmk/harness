package com.evolopy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestBenchmarksEdge {

    @Test
    public void testProdEmpty() {
        int[] arr = {};
        int prod = 1;
        for (int v : arr) prod *= v;
        assertEquals(1, prod);
    }

    @Test
    public void testProdMultiple() {
        int[] arr = {2, 3, 4};
        int prod = 1; for (int v : arr) prod *= v;
        assertEquals(24, prod);
    }
}