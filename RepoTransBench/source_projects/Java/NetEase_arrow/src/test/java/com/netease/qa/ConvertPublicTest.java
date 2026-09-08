package com.netease.qa;

import org.junit.*;
import java.io.*;
import org.apache.commons.io.FileUtils;
import static org.junit.Assert.*;

public class ConvertPublicTest {

    private File gbkFile;
    private File utf8File;

    @Before
    public void setUp() throws Exception {
        gbkFile = File.createTempFile("public_testfile", ".txt");
        utf8File = File.createTempFile("public_utf8file", ".txt");
        // Write different Chinese characters "世界" (means "world") in GBK encoding
        FileOutputStream fos = new FileOutputStream(gbkFile);
        fos.write("世界".getBytes("GBK"));
        fos.close();
        if (utf8File.exists()) utf8File.delete();
    }

    @After
    public void tearDown() throws Exception {
        if (gbkFile.exists()) gbkFile.delete();
        if (utf8File.exists()) utf8File.delete();
        File tmp = new File(gbkFile.getAbsolutePath() + ".tmp");
        if (tmp.exists()) tmp.delete();
    }

    @Test
    public void testConvertGbkToUtf8InPlace() throws Exception {
        String[] args = {gbkFile.getAbsolutePath()};
        Convert.main(args);
        // File should remain (be replaced). Read as UTF-8.
        String content = FileUtils.readFileToString(gbkFile, "UTF-8");
        assertTrue(content.contains("世界"));
    }

    @Test
    public void testConvertGbkToUtf8WithDifferentOutputFile() throws Exception {
        String[] args = {gbkFile.getAbsolutePath(), utf8File.getAbsolutePath()};
        Convert.main(args);
        assertTrue(utf8File.exists());
        String content = FileUtils.readFileToString(utf8File, "UTF-8");
        assertTrue(content.contains("世界"));
    }

    @Test
    public void testIOExceptionIsHandled() throws Exception {
        // Use a definitely non-existent file to trigger IOException (different path)
        String[] args = {"/definitely/doesnotexist/inputfile_public.txt"};
        // Should not throw, just print stack trace
        Convert.main(args);
    }
}