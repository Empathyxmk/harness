package org.example;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CheckTargetTest {

    @Test
    void testIsValid() {
        assertTrue(CheckTarget.isValid("http://test.com"));
        assertFalse(CheckTarget.isValid("invalid_string"));
        assertFalse(CheckTarget.isValid(""));
    }

    @Test
    void testSanitize() {
        assertEquals("abc", CheckTarget.sanitize("abc"));
        assertEquals("", CheckTarget.sanitize(null));
    }
}