package com.example.arff.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestData {

    @Test
    void testSimpleData() {
        List<Object> row = Arrays.asList("x", 42, null);
        assertEquals("x", row.get(0));
        assertEquals(42, row.get(1));
        assertNull(row.get(2));
    }

    @Test
    void testDataWithStringsAndInts() {
        List<List<Object>> data = Arrays.asList(
            Arrays.asList("a", 5),
            Arrays.asList("b", 10)
        );
        assertEquals("a", data.get(0).get(0));
        assertEquals(10, data.get(1).get(1));
    }
}