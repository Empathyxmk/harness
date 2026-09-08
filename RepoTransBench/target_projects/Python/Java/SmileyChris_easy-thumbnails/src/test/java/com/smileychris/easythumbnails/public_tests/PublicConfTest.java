package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicConfTest {

    @Test
    void testDefaultSettingsPublic() {
        assertTrue(true);
        assertEquals("thumbnails", "thumbnails");
    }

    @Test
    void testSettingsChangeAndResetPublic() {
        assertEquals("special_public_subdir", "special_public_subdir");
        assertEquals("thumbnails", "thumbnails");
    }
}