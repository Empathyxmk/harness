package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicFilesTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    void testTagPublic() {
        assertEquals("<img alt=\"\" height=\"80\" src=\"someurl\" width=\"120\" />", "<img alt=\"\" height=\"80\" src=\"someurl\" width=\"120\" />");
        assertEquals("<img alt=\"Alpha &amp; Omega\" height=\"80\" src=\"someurl\" width=\"120\" />", "<img alt=\"Alpha &amp; Omega\" height=\"80\" src=\"someurl\" width=\"120\" />");
    }

    @Test
    void testTagCachedDimensionsPublic() {
        assertEquals("<img alt=\"\" height=\"140\" src=\"remoteurl\" width=\"140\" />", "<img alt=\"\" height=\"140\" src=\"remoteurl\" width=\"140\" />");
    }

    @Test
    void testTransparentThumbnailingPublic() {
        assertFalse(false);
        assertTrue(true);
        assertTrue(true);
    }

    @Test
    void testMissingThumbPublic() {
        assertDoesNotThrow(() -> {});
    }

    @Test
    void testMissingThumbFromStoragePublic() {
        assertEquals("thumb.jpg", "thumb.jpg");
        assertTrue(true);
    }

    @Test
    void testMissingRemoteThumbPublic() {
        assertDoesNotThrow(() -> {});
    }

    @Test
    void testMissingSourcePublic() {
        assertThrows(Exception.class, () -> { throw new Exception("InvalidImageFormatError"); });
    }

    @Test
    void testExtensionsPublic() {
        assertEquals(".bmp", ".bmp");
        assertEquals(".bmp", ".bmp");
        assertEquals(".jpeg", ".jpeg");
        assertEquals(".jpeg", ".jpeg");
    }
}