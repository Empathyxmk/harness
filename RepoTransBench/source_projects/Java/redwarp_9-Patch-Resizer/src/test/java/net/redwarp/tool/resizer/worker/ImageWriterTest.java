package net.redwarp.tool.resizer.worker;

import org.junit.*;

import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import java.io.*;

import static org.junit.Assert.*;

public class ImageWriterTest {

    private BufferedImage img;
    private File outputFile;
    private File inputFile;

    @Before
    public void setUp() throws IOException {
        img = new BufferedImage(10, 10, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = img.createGraphics();
        g.drawLine(0, 0, 9, 9);
        g.dispose();
        outputFile = File.createTempFile("testimg", ".png");
        inputFile = File.createTempFile("testimginput", ".png");
        ImageIO.write(img, "png", inputFile);
    }

    @After
    public void tearDown() {
        if (outputFile != null) outputFile.delete();
        if (inputFile != null) inputFile.delete();
    }

    @Test
    public void testWritePNG() throws IOException {
        ImageWriter.write(img, Output.PNG, outputFile);
        assertTrue(outputFile.exists());
        // Load it back, ensure it's an image
        BufferedImage loaded = ImageIO.read(outputFile);
        assertNotNull(loaded);
        assertEquals(img.getWidth(), loaded.getWidth());
        assertEquals(img.getHeight(), loaded.getHeight());
    }

    @Test
    public void testWriteJPG() throws IOException {
        File jpgOutput = File.createTempFile("testimg", ".jpg");
        try {
            ImageWriter.write(img, Output.JPG, jpgOutput);
            assertTrue(jpgOutput.exists());
            BufferedImage loaded = ImageIO.read(jpgOutput);
            assertNotNull(loaded);
            assertEquals(img.getWidth(), loaded.getWidth());
            assertEquals(img.getHeight(), loaded.getHeight());
        } finally {
            jpgOutput.delete();
        }
    }

    @Test
    public void testCopy() throws IOException {
        File copyFile = File.createTempFile("copyimg", ".png");
        try {
            ImageWriter.copy(inputFile, copyFile);
            assertTrue(copyFile.exists());
            BufferedImage loaded = ImageIO.read(copyFile);
            assertNotNull(loaded);
        } finally {
            copyFile.delete();
        }
    }
    
    @Test
    public void testCopyNullInputs() throws IOException {
        // Should do nothing, no exception
        ImageWriter.copy(null, null);
    }
}