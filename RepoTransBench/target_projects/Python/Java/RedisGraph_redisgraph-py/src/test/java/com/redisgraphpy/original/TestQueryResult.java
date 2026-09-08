// Supplemental test for test_query_result.py, beyond QueryResultTest.java.
package com.redisgraphpy.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

class TestQueryResult {

    @Test
    void testEmptyQueryResult() {
        QueryResult qr = new QueryResult(List.of(), List.of(), Map.of());
        assertEquals(0, qr.size());
        assertTrue(qr.getStatistics().isEmpty());
    }
}