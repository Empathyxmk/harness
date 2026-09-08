package com.example.protontricks.public;

import org.junit.jupiter.api.Test;

// Ensures public_tests is treated as a package for test discovery when needed.
class PublicInitTest {
    @Test
    void testPublicInitDummy() {
        // This test exists to make the package non-empty and discoverable.
        // Other real public tests reside in other files.
        // No assertions needed.
    }
}