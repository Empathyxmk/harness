package net.yacy.grid.search;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SearchPublicTest {

    @Test
    void testQueryNormal() {
        Search s = new Search();
        assertEquals("Search results for: world", s.query("world"));
        assertEquals("Search results for: 123", s.query("123"));
        assertEquals("Search results for: test_case", s.query("test_case"));
    }

    @Test
    void testQueryEmptyVariants() {
        Search s = new Search();
        assertEquals("No query provided", s.query("   ")); // only spaces
        assertEquals("No query provided", s.query(null));
        assertEquals("No query provided", s.query("\t")); // tab only
    }

    @Test
    void testQueryErrorDifferentCase() {
        Search s = new Search();
        Exception ex = assertThrows(IllegalArgumentException.class, () -> s.query("ERROR"));
        assertEquals("Invalid query", ex.getMessage());
        Exception ex2 = assertThrows(IllegalArgumentException.class, () -> s.query("Error"));
        assertEquals("Invalid query", ex2.getMessage());
    }

    @Test
    void testIsServiceActiveStillTrue() {
        Search s = new Search();
        assertTrue(s.isServiceActive());
    }
}