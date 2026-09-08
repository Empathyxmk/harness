package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class QueryResultExtraTest {

    @Test
    void testQueryResultToString() {
        QueryResult qr = new QueryResult(java.util.List.of("id"), java.util.List.of(java.util.List.of(1)), java.util.Map.of());
        assertTrue(qr.toString().contains("id"));
    }

    @Test
    void testQueryResultEqualsAndHash() {
        QueryResult qr1 = new QueryResult(java.util.List.of("id"), java.util.List.of(java.util.List.of(1)), java.util.Map.of());
        QueryResult qr2 = new QueryResult(java.util.List.of("id"), java.util.List.of(java.util.List.of(1)), java.util.Map.of());
        assertEquals(qr1, qr2);
        assertEquals(qr1.hashCode(), qr2.hashCode());
    }
}