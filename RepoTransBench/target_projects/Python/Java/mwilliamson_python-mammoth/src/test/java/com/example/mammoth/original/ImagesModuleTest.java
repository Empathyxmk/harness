package com.example.mammoth.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ImagesModuleTest {
    @Test
    void testImageUrl() {
        Image image = new Image("http://foo/img.png", 100, 200);
        assertEquals("http://foo/img.png", image.getUrl());
        assertEquals(100, image.getWidth());
        assertEquals(200, image.getHeight());
    }

    @Test
    void testImageResize() {
        Image image = new Image("http://bar/img.jpg", 320, 240);
        image.resize(160, 120);
        assertEquals(160, image.getWidth());
        assertEquals(120, image.getHeight());
    }

    static class Image {
        private String url;
        private int width;
        private int height;
        Image(String url, int width, int height) {
            this.url = url;
            this.width = width;
            this.height = height;
        }
        String getUrl() { return url; }
        int getWidth() { return width; }
        int getHeight() { return height; }
        void resize(int w, int h) {
            this.width = w;
            this.height = h;
        }
    }
}