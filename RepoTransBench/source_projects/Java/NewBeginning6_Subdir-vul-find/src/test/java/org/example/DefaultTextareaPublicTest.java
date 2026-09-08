package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DefaultTextareaPublicTest {

    @Test
    void testGetDefault() {
        String val = DefaultTextarea.getDefault();
        assertNotNull(val);
        assertTrue(val.trim().length() > 0);
    }
}