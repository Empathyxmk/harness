package com.aiforever.gigachat.publicapi;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class Image {
    String url;
    int width;
    int height;

    public Image(String url, int width, int height) {
        this.url = url;
        this.width = width;
        this.height = height;
    }
}

public class PublicImagesTest {

    @Test
    void testImageCreation() {
        Image img = new Image("http://image.com/pic.jpg", 800, 600);
        assertEquals("http://image.com/pic.jpg", img.url);
        assertEquals(800, img.width);
        assertEquals(600, img.height);
    }

    @Test
    void testImageAspectRatio() {
        Image img = new Image("url", 1024, 512);
        double ratio = (double) img.width / img.height;
        assertEquals(2.0, ratio);
    }
}