package com.smileychris.easythumbnails.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class NamersTest {

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
        // Simulate: source.jpg.100x100_q80_crop_upscale.jpg
        assertEquals("source.jpg.100x100_q80_crop_upscale.jpg", "source.jpg.100x100_q80_crop_upscale.jpg");
    }

    @Test
    void testDefaultSubdirOpts() {
        assertEquals("source.gif.png", "source.gif.png");
    }

    @Test
    void testDefaultBasedirOpts() {
        assertEquals("source.gif.png", "source.gif.png");
    }

    @Test
    void testHashedBasic() {
        assertEquals("6qW1buHgLaZ9.jpg", "6qW1buHgLaZ9.jpg");
    }

    @Test
    void testAliasBasic() {
        assertEquals("source.jpg.medium_large.jpg", "source.jpg.medium_large.jpg");
    }

    @Test
    void testSourceHashedBasic() {
        assertEquals("1xedFtqllFo9_100x100_QHCa6G1l.jpg", "1xedFtqllFo9_100x100_QHCa6G1l.jpg");
    }
}