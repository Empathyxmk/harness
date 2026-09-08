package com.packtpublishing.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class OriginalTestPytestCleanupTest {

    static int resource;

    @BeforeAll
    static void setupResource() {
        resource = 42;
    }

    @Test
    void testResourceAvailable() {
        assertEquals(42, resource);
    }

    @AfterAll
    static void cleanupResource() {
        resource = 0;
    }
}