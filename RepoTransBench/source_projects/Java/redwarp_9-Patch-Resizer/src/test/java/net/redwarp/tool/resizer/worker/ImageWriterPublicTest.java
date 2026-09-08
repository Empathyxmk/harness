package net.redwarp.tool.resizer.worker;

import org.junit.*;

import java.awt.image.BufferedImage;
import java.awt.Graphics2D;
import java.io.*;

import static org.junit.Assert.*;
import javax.imageio.ImageIO;

public class ImageWriterPublicTest {

    private BufferedImage img;
    private File outputFile;
    private File inputFile;

    @Before
    public void setUp() throws IOException {
        img = new BufferedImage(15, 8, BufferedImage.TYPE_INT_RGB);
        Graphics2D g = img.createGraphics();
        g.fillRect(1, 1, 13, 6);
        g.drawRect(0, 0, 14, 7);
        g.dispose();
        outputFile = File.createTempFile("pubimg", ".png");
        inputFile = File.createTempFile("pubimginput", ".png");
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
        BufferedImage loaded = ImageIO.read(outputFile);
        assertNotNull(loaded);
        assertEquals(img.getWidth(), loaded.getWidth());
        assertEquals(img.getHeight(), loaded.getHeight());
    }

    @Test
    public void testWriteJPG() throws IOException {
        File jpgOutput = File.createTempFile("pubimg", ".jpg");
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
        File copyFile = File.createTempFile("cpubimg", ".png");
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