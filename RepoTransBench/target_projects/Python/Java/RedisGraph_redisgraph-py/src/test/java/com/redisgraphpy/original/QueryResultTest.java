package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class QueryResultTest {
    @Test
    void testQueryResultRow() {
        List<String> header = List.of("name", "age");
        List<Object> row = List.of("Alice", 30);
        QueryResult qr = new QueryResult(header, List.of(row), Map.of());
        assertEquals(1, qr.size());
        assertEquals("Alice", qr.getRow(0).get(0));
    }

    @Test
    void testQueryResultStatistics() {
        QueryResult qr = new QueryResult(List.of(), List.of(), Map.of("labels-added", 2));
        assertEquals(2, qr.getStatistics().get("labels-added"));
    }
}