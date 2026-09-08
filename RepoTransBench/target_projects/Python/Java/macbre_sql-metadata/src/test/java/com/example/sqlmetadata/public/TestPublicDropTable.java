package com.example.sqlmetadata.public;

import com.example.sqlmetadata.Parser;
import com.example.sqlmetadata.keywords.QueryType;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * Translated from public_tests/test_public_drop_table.py
 */
public class TestPublicDropTable {
    @Test
    public void testPublicDropTable() {
        Parser parser = new Parser("DROP TABLE bar");
        assertEquals(QueryType.DROP, parser.getQueryType());
        assertEquals(List.of("bar"), parser.getTables());
        assertTrue(parser.getColumns().isEmpty());
    }
}