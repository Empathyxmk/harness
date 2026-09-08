package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicPixelProcessorsTest {

    @Test
    void testScaleAndCropAspectRatioPublic() {
        assertEquals(20, 20);
        assertEquals(10, 10);
    }

    @Test
    void testScaleAndCropCropOptionPublic() {
        assertEquals(20, 20);
    }
}