package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicWarnings {

    @Test
    public void testWarningString() {
        String warning = "Warning: something happened";
        assertEquals("Warning: something happened", warning);
    }
}