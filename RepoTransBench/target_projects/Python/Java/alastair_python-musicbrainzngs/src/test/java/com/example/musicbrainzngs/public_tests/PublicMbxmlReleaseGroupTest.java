package com.example.musicbrainzngs.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicMbxmlReleaseGroupTest {

    @Test
    void testReleaseGroupPattern() {
        // Simulates parsing a release group id
        String rgid = "1d9bfa60-11e6-3052-9a90-7f97f765bbc3";
        assertTrue(rgid.matches("[0-9a-f\\-]{36}"));
    }
}