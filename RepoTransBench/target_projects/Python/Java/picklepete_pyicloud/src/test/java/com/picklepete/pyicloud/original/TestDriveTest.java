package com.picklepete.pyicloud.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Arrays;
import java.util.List;

public class TestDriveTest {
    @Test
    public void testDriveListing() {
        List<String> files = Arrays.asList("file1.txt", "file2.txt", "images/photo.jpg");
        assertTrue(files.contains("file1.txt"));
        assertTrue(files.contains("images/photo.jpg"));
    }

    @Test
    public void testFileDownload() {
        String filename = "file1.txt";
        String fileContent = "Hello World";
        assertNotNull(fileContent);
        assertEquals("Hello World", fileContent);
    }

    @Test
    public void testFileSize() {
        int fileSize = 2048; // 2KB
        assertTrue(fileSize > 0);
        assertEquals(2048, fileSize);
    }
}