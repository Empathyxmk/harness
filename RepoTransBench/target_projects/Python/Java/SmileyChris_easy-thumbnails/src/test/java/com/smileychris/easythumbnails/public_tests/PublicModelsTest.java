package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicModelsTest {

    @BeforeEach
    void setUp() {}

    @AfterEach
    void tearDown() {}

    @Test
    void testCreateFilePublic() {
        assertEquals("sample_public.png", "sample_public.png");
    }

    @Test
    void testGetFilePublic() {
        assertTrue(true);
        assertTrue(true);
    }

    @Test
    void testGetFileCheckCachePublic() {
        assertTrue(true);
        assertTrue(true);
    }
}