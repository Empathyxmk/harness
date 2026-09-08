package net.yacy.grid.search;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SearchTest {

    @Test
    void testQueryNormal() {
        Search s = new Search();
        assertEquals("Search results for: hello", s.query("hello"));
    }

    @Test
    void testQueryEmpty() {
        Search s = new Search();
        assertEquals("No query provided", s.query(""));
        assertEquals("No query provided", s.query(null));
        assertEquals("No query provided", s.query("  "));
    }

    @Test
    void testQueryError() {
        Search s = new Search();
        Exception ex = assertThrows(IllegalArgumentException.class, () -> s.query("error"));
        assertEquals("Invalid query", ex.getMessage());
    }

    @Test
    void testIsServiceActive() {
        Search s = new Search();
        assertTrue(s.isServiceActive());
    }
}