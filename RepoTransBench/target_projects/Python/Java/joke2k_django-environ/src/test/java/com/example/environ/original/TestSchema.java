package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestSchema {

    @Test
    void testSchemaUrl() {
        assertTrue(SchemaUtils.isUrl("postgres://user@localhost:5432/dbname"));
        assertFalse(SchemaUtils.isUrl("notadatabaseurl"));
    }

    @Test
    void testParseDatabaseUrl() {
        DatabaseUrlInfo info = SchemaUtils.parseDatabaseUrl("postgres://user:pass@host:5432/dbname");
        assertEquals("postgres", info.getEngine());
        assertEquals("user", info.getUser());
        assertEquals("pass", info.getPassword());
        assertEquals("host", info.getHost());
        assertEquals(5432, info.getPort());
        assertEquals("dbname", info.getDatabase());
    }
}