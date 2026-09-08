package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicQueryResultExtraTest {

    @Test
    void testPublicQueryResultToString() {
        QueryResult qr = new QueryResult(java.util.List.of("id"), java.util.List.of(java.util.List.of(1)), java.util.Map.of());
        assertTrue(qr.toString().contains("id"));
    }
}