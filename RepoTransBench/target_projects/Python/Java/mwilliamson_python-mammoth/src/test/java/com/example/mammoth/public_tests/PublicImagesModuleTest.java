package com.example.mammoth.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicImagesModuleTest {
    @Test
    void testPublicImage() {
        Image image = new Image("img.png");
        assertEquals("img.png", image.getUrl());
    }

    static class Image {
        private final String url;
        Image(String url) { this.url = url; }
        String getUrl() { return url; }
    }
}