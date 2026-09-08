package com.example.musicbrainzngs.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicMbxmlArtistTest {

    @Test
    void testArtistIdPattern() {
        // Checks if a test artist id follows expected MusicBrainz UUID pattern
        String artistId = "0e43fe9d-c472-4b62-be9e-55f971a023e1";
        assertEquals(36, artistId.length());
        assertTrue(artistId.matches("[0-9a-f\\-]{36}"));
    }
}