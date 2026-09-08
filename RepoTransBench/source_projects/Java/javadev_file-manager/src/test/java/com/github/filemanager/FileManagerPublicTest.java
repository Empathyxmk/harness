package com.github.filemanager;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;

public class FileManagerPublicTest {

    private FileManager fm;
    // Use different file names for public tests
    private final String publicTestFile = "public_sample.txt";
    private final String publicCopiedFile = "public_copied.txt";
    private final String publicNullFile = null;

    @Before
    public void setUp() {
        fm = new FileManager();
    }

    @After
    public void tearDown() {
        File f1 = new File(publicTestFile);
        if (f1.exists()) f1.delete();
        File f2 = new File(publicCopiedFile);
        if (f2.exists()) f2.delete();
        File f3 = new File("unused_public.txt");
        if (f3.exists()) f3.delete();
        File f4 = new File("another_public.txt");
        if (f4.exists()) f4.delete();
    }

    @Test
    public void testFileExists_false_public() {
        assertFalse(fm.fileExists("definitelynotexisting_public.txt"));
    }

    @Test
    public void testFileExists_true_public() throws IOException {
        File f = new File(publicTestFile);
        assertTrue(f.createNewFile());
        assertTrue(fm.fileExists(publicTestFile));
    }

    @Test
    public void testFileExists_null_public() {
        assertFalse(fm.fileExists(null));
    }

    @Test
    public void testCreateFile_success_public() throws IOException {
        assertTrue(fm.createFile(publicTestFile));
        // Creating again should return false (already exists)
        assertFalse(fm.createFile(publicTestFile));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCreateFile_null_public() throws IOException {
        fm.createFile(publicNullFile);
    }

    @Test
    public void testDeleteFile_exists_public() throws IOException {
        File f = new File(publicTestFile);
        f.createNewFile();
        assertTrue(fm.deleteFile(publicTestFile));
        // File should not exist after deletion
        assertFalse(new File(publicTestFile).exists());
    }

    @Test
    public void testDeleteFile_notExists_public() {
        assertFalse(fm.deleteFile("unused_public.txt"));
    }

    @Test
    public void testDeleteFile_null_public() {
        assertFalse(fm.deleteFile(publicNullFile));
    }

    @Test
    public void testCopyFile_success_public() throws IOException {
        File f = new File(publicTestFile);
        f.createNewFile();
        assertTrue(fm.copyFile(publicTestFile, publicCopiedFile));
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCopyFile_sourceNull_public() throws IOException {
        fm.copyFile(null, "another_public.txt");
    }

    @Test(expected = IllegalArgumentException.class)
    public void testCopyFile_destNull_public() throws IOException {
        fm.copyFile("another_public.txt", null);
    }
}