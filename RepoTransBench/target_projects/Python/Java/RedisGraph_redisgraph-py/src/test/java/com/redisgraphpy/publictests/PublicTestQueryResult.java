package com.redisgraphpy.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Map;

class PublicTestQueryResult {

    @Test
    void testPublicQueryResultStatistics() {
        QueryResult qr = new QueryResult(List.of(), List.of(), Map.of("rows-generated", 5));
        assertEquals(5, qr.getStatistics().get("rows-generated"));
    }
}