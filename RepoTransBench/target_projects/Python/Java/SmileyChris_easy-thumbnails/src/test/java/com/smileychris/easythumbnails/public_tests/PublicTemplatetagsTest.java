package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class PublicTemplatetagsTest {

    @Test
    void testThumbnailerFilterRenderPublic() {
        assertTrue("abc.jpg".contains(".jpg"));
        assertTrue("150x75".contains("150x75"));
    }

    @Test
    void testThumbnailTagImgpathPublic() {
        assertTrue("xyz.jpg".contains("xyz.jpg") && "60x90".contains("60x90"));
    }
}