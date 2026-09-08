package org.example;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class DefaultTextTest {

    @Test
    void testGetDefault() {
        String val = DefaultText.getDefault();
        assertNotNull(val);
        assertFalse(val.isEmpty());
    }
}