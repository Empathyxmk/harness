package com.github.filemanager;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;

public class FileManagerTest {

    private FileManager fm;
    private final String testFile = "testfile.txt";
    private final String copiedFile = "copiedfile.txt";
    private final String nullFile = null;

    @Before
    public void setUp() {
        fm = new FileManager();
    }

    @After
    public void tearDown() {
        File f1 = new File(testFile);
        if (f1.exists()) f1.delete();
        File f2 = new File(copiedFile);
        if (f2.exists()) f2.delete();
        File f3 = new File("dummy.txt");
        if (f3.exists()) f3.delete();
    }

    @Test
    public void testFileExists_false() {
        assertFalse(fm.fileExists("notreallypresent.txt"));
    }

    @Test
    public void testFileExists_true() throws IOException {
        File f = new File(testFile);
        assertTrue(f.createNewFile());
        assertTrue(fm.fileExists(testFile));
    }

    @Test
    public void testFileExists_null() {
        assertFalse(fm.fileExists(null));
    }

    @Test
    public void testCreateFile_success() throws IOException {
        assertTrue(fm.createFile(testFile));
        // Creating again should return false (already exists)
        assertFalse(fm.createFile(testFile));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCreateFile_null() throws IOException {
        fm.createFile(nullFile);
    }

    @Test
    public void testDeleteFile_exists() throws IOException {
        File f = new File(testFile);
        f.createNewFile();
        assertTrue(fm.deleteFile(testFile));
        // File should not exist after deletion
        assertFalse(new File(testFile).exists());
    }

    @Test
    public void testDeleteFile_notExists() {
        assertFalse(fm.deleteFile("dummy.txt"));
    }

    @Test
    public void testDeleteFile_null() {
        assertFalse(fm.deleteFile(nullFile));
    }

    @Test
    public void testCopyFile_success() throws IOException {
        File f = new File(testFile);
        f.createNewFile();
        assertTrue(fm.copyFile(testFile, copiedFile));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCopyFile_sourceNull() throws IOException {
        fm.copyFile(null, "dest.txt");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCopyFile_destNull() throws IOException {
        fm.copyFile("src.txt", null);
    }
}