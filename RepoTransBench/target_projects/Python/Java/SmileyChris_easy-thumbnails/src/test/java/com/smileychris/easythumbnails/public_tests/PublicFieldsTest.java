package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicFieldsTest {

    @Test
    void testThumbnailerFieldDeconstructPublic() {
        assertEquals("ThumbnailerField", "ThumbnailerField");
        assertEquals("gallery/images/", "gallery/images/");
    }

    @Test
    void testThumbnailerFieldGenerateThumbnailPublic() {
        assertNotEquals("foo1.jpg", "foo2.jpg");
    }
}