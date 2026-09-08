package com.example.environ.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class TestDB {

    @Test
    void testParseDefault() {
        DBConfig db = DBConfig.defaultConfig();
        assertEquals("sqlite", db.getEngine());
        assertEquals("db.sqlite3", db.getName());
    }

    @Test
    void testParsePostgres() {
        DBConfig db = DBConfig.fromUrl("postgres://user:pass@host:5432/dbname");
        assertEquals("postgres", db.getEngine());
        assertEquals("user", db.getUser());
        assertEquals("pass", db.getPassword());
        assertEquals("host", db.getHost());
        assertEquals(5432, db.getPort());
        assertEquals("dbname", db.getName());
    }
}