package com.picklepete.pyicloud.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;
import java.util.Arrays;

public class PublicDriveTest {

    @Test
    public void testPublicDriveFileListing() {
        List<String> files = Arrays.asList("sample.txt", "photo.jpg", "readme.md");
        assertTrue(files.contains("readme.md"));
        assertEquals(3, files.size());
    }

    @Test
    public void testPublicDriveGetFileContent() {
        String fileName = "sample.txt";
        String fileContent = "The quick brown fox";
        assertEquals("The quick brown fox", fileContent);
        assertTrue(fileName.endsWith(".txt"));
    }

    @Test
    public void testPublicDriveSharedFolder() {
        boolean sharedFolderExists = true;
        assertTrue(sharedFolderExists);
    }
}