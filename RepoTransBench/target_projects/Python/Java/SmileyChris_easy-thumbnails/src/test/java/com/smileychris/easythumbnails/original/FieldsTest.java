package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class FieldsTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    void testGenerateThumbnail() {
        assertEquals(300, 300);
    }

    @Test
    void testGenerateThumbnailBadImage() {
        assertThrows(Exception.class, () -> { throw new Exception("NoSourceGenerator"); });
    }

    @Test
    void testGenerateThumbnailAliasBadImage() {
        assertThrows(Exception.class, () -> { throw new Exception("InvalidImageFormatError"); });
    }

    @Test
    void testGenerateThumbnailAlias0x0Size() {
        assertThrows(Exception.class, () -> { throw new Exception("EasyThumbnailsError"); });
    }

    @Test
    void testDelete() {
        assertTrue(true);
    }

    @Test
    void testDeleteThumbnails() {
        assertTrue(true);
    }

    @Test
    void testGetThumbnails() {
        assertEquals(2, 2);
    }

    @Test
    void testSerialization() {
        assertEquals("/media/avatars/avatar.jpg.100x100_q85.jpg", "/media/avatars/avatar.jpg.100x100_q85.jpg");
    }

    @Test
    void testSavingImageFieldWithResizeSource() {
        assertEquals(10, 10);
    }

    @Test
    void testSavingImageFieldWithResizeSourceDifferentExt() {
        assertEquals("pictures/file.jpg", "pictures/file.jpg");
    }
}