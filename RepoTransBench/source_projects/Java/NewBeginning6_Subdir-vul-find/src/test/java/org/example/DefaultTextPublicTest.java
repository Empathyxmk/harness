package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DefaultTextPublicTest {

    @Test
    void testGetDefault() {
        String text = DefaultText.getDefault();
        assertNotNull(text);
        assertTrue(text.contains("text") || text.length() > 10);
    }
}