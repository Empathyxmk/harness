package com.jude.utils;

// Placeholder for public JFileManager tests.
// Actual tests must use different test data compared to existing JFileManagerTest.

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class JFileManagerPublicTest {

    @Test
    void testFilePathExtractionPublic() {
        // Assuming JFileManager has a method getFileNameFromPath(String)
        String filePath = "/storage/emulated/0/Download/public_test_file2.txt";
        String fileName = JFileManager.getFileNameFromPath(filePath);
        assertEquals("public_test_file2.txt", fileName);
    }

    @Test
    void testGetFileExtensionPublic() {
        // Assuming JFileManager has a method getFileExtension(String)
        String fileName = "sample_document.data";
        String extension = JFileManager.getFileExtension(fileName);
        assertEquals("data", extension);
    }

    @Test
    void testIsPathAbsolutePublic() {
        // Assuming JFileManager has a static method isAbsolutePath(String)
        String path = "/home/user/example";
        assertTrue(JFileManager.isAbsolutePath(path));

        String relPath = "docs/readme.txt";
        assertFalse(JFileManager.isAbsolutePath(relPath));
    }
}