package com.example.arff.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.*;

class TestPublicData {

    @Test
    void testPublicDataRow() {
        List<Object> row = Arrays.asList("bar", 5, null);
        assertEquals("bar", row.get(0));
        assertEquals(5, row.get(1));
        assertNull(row.get(2));
    }

    @Test
    void testPublicDataList() {
        List<List<Object>> data = Arrays.asList(
            Arrays.asList("a", 3),
            Arrays.asList("b", 7)
        );
        assertEquals("a", data.get(0).get(0));
        assertEquals(7, data.get(1).get(1));
    }
}