package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class CheckTargetPublicTest {

    @Test
    void testIsValidUrl() {
        assertTrue(CheckTarget.isTarget("https://www.wikipedia.org"));
        assertTrue(CheckTarget.isTarget("http://localhost:8000/test"));
        assertFalse(CheckTarget.isTarget("file:///tmp/test.txt"));
        assertFalse(CheckTarget.isTarget("not_a_url"));
    }

    @Test
    void testHostLogic() {
        assertEquals("example.com", CheckTarget.Host("http://example.com/page"));
        assertEquals("localhost", CheckTarget.Host("https://localhost:1234"));
        assertEquals("", CheckTarget.Host("file:///tmp/test.txt"));
    }
}