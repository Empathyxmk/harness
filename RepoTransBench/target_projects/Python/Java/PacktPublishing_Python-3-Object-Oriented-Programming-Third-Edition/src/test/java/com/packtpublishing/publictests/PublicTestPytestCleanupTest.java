package com.packtpublishing.publictests;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicTestPytestCleanupTest {
    static int shared;

    @BeforeAll
    static void setup() {
        shared = 7;
    }

    @Test
    void testSharedIs7() {
        assertEquals(7, shared);
    }

    @AfterAll
    static void cleanup() {
        shared = 0;
    }
}