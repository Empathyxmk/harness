package com.example.original;

import com.example.haishoku.haillow.Haillow;
import org.junit.jupiter.api.*;
import java.io.File;
import java.io.IOException;
import static org.junit.jupiter.api.Assertions.*;

public class TestHaillow {

    private File tmpFile;

    @BeforeEach
    public void setUp() throws IOException {
        // Simulate creating an image file; skip or stub as needed
        tmpFile = File.createTempFile("test_img", ".png");
        tmpFile.deleteOnExit();
    }

    @AfterEach
    public void tearDown() {
        if(tmpFile != null && tmpFile.exists()) {
            tmpFile.delete();
        }
    }

    @Test
    public void testGetImageLocal() {
        Object img = Haillow.getImage(tmpFile.getAbsolutePath());
        assertNotNull(img);
        assertEquals("RGB", Haillow.getMode(img));
    }

    @Test
    public void testGetImageConvert() throws IOException {
        File grayFile = new File(tmpFile.getAbsolutePath() + "_gray.png");
        grayFile.createNewFile();
        Object img = Haillow.getImage(grayFile.getAbsolutePath());
        assertEquals("RGB", Haillow.getMode(img));
        grayFile.delete();
    }

    @Test
    public void testGetThumbnail() {
        Object img = Haillow.getImage(tmpFile.getAbsolutePath());
        Object thumb = Haillow.getThumbnail(img);
        assertTrue(Haillow.getWidth(thumb) <= 256);
        assertTrue(Haillow.getHeight(thumb) <= 256);
    }

    @Test
    public void testGetColors() {
        Object colors = Haillow.getColors(tmpFile.getAbsolutePath());
        assertNotNull(colors);
    }

    @Test
    public void testNewImage() {
        Object img = Haillow.newImage("RGB", 8, 9, new int[]{1,2,3});
        assertEquals(8, Haillow.getWidth(img));
        assertEquals(9, Haillow.getHeight(img));
    }

    @Test
    public void testJointImage() {
        Object[] imgs = new Object[4];
        for(int i=0; i<4; i++)
            imgs[i] = Haillow.newImage("RGB", 50, 20, new int[]{i*20, 0, i*30});
        try {
            Haillow.jointImage(imgs);
        } catch(Exception e) {
            fail("jointImage failed: " + e.getMessage());
        }
    }
}