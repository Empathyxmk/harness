package com.netease.qa;

import org.junit.*;
import java.io.*;
import org.apache.commons.io.FileUtils;
import static org.junit.Assert.*;

public class ConvertTest {

    private File gbkFile;
    private File utf8File;

    @Before
    public void setUp() throws Exception {
        gbkFile = File.createTempFile("testfile", ".txt");
        utf8File = File.createTempFile("utf8file", ".txt");
        // Write Chinese characters "你好" in GBK encoding
        FileOutputStream fos = new FileOutputStream(gbkFile);
        fos.write("你好".getBytes("GBK"));
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
        assertTrue(content.contains("你好"));
    }

    @Test
    public void testConvertGbkToUtf8WithDifferentOutputFile() throws Exception {
        String[] args = {gbkFile.getAbsolutePath(), utf8File.getAbsolutePath()};
        Convert.main(args);
        assertTrue(utf8File.exists());
        String content = FileUtils.readFileToString(utf8File, "UTF-8");
        assertTrue(content.contains("你好"));
    }

    @Test
    public void testIOExceptionIsHandled() throws Exception {
        // Use a non-existent file to trigger IOException
        String[] args = {"/not/exists/input/file.txt"};
        // Should not throw, just print stack trace
        Convert.main(args);
    }
}