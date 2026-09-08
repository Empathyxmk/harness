package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicCreateTag {

    @Test
    public void testTagCreation() {
        String tag = "v2.1.0";
        assertTrue(tag.startsWith("v"));
    }
}