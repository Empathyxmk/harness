package com.example.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class TestPublicClassImport {

    @Test
    public void testClassImport() {
        boolean importWorked = true;
        assertTrue(importWorked, "Class import did not work.");
    }
}