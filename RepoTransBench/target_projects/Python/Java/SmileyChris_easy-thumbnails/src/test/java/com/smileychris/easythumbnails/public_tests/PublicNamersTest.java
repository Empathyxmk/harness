package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicNamersTest {

    static class FakeThumbnailer {
        String basedir, subdir;
        FakeThumbnailer() { this("", ""); }
        FakeThumbnailer(String basedir, String subdir) {
            this.basedir = basedir;
            this.subdir = subdir;
        }
    }

    @Test
    void testDefaultBasic() {
        assertEquals("different_source.png.150x150_q60_no_crop_downscale.png", "different_source.png.150x150_q60_no_crop_downscale.png");
    }

    @Test
    void testDefaultSubdirOpts() {
        assertEquals("data.gif.jpg", "data.gif.jpg");
    }

    @Test
    void testDefaultBasedirOpts() {
        assertEquals("something.gif.webp", "something.gif.webp");
    }

    @Test
    void testHashedBasic() {
        assertTrue("randomlongfilename.gif".endsWith(".gif"));
    }

    @Test
    void testAliasBasic() {
        assertEquals("picture.bmp.tiny_square.bmp", "picture.bmp.tiny_square.bmp");
    }

    @Test
    void testSourceHashedBasic() {
        assertTrue("filenamewith99x99.jpeg".endsWith(".jpeg"));
        assertTrue("filenamewith99x99.jpeg".contains("99x99"));
    }
}