package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DefaultTextareaTest {

    @Test
    void testGetDefault() {
        String val = DefaultTextarea.getDefault();
        assertNotNull(val);
        assertFalse(val.isEmpty());
    }
}