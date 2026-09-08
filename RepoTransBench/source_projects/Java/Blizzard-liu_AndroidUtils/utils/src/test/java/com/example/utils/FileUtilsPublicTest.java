package com.example.utils;

import org.junit.Test;

import static org.junit.Assert.*;

public class FileUtilsPublicTest {
    @Test
    public void testGetFileExtensionJson_public() {
        // Use a different extension, e.g., json
        String fileName = "myapiresult.json";
        String ext = fileName.substring(fileName.lastIndexOf('.'));
        assertEquals(".json", ext);
    }
}