package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicConfigPy {

    @Test
    public void testConfigValue() {
        String config = "default";
        assertEquals("default", config);
    }
}