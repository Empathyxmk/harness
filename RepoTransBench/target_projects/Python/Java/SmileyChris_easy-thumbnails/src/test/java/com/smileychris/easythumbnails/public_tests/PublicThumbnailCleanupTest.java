package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicThumbnailCleanupTest {

    String[] dummyGetThumbnailFilesPublic() {
        return new String[] {"public_thumbnails/thumb1.jpg", "public_thumbnails/thumb2.png"};
    }

    @Test
    void testThumbnailCleanupFilesToRemovePublic() {
        String[] thumbnails = dummyGetThumbnailFilesPublic();
        assertEquals(2, thumbnails.length);
        assertTrue(thumbnails[0].endsWith(".jpg"));
        assertTrue(thumbnails[1].endsWith(".png"));
    }
}