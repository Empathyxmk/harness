package com.example.utils;

import org.junit.Test;

import java.io.File;
import java.io.FileOutputStream;
import java.io.ByteArrayInputStream;
import java.io.InputStream;

import static org.junit.Assert.*;

public class FileUtilsTest {

    @Test
    public void testWriteAndReadFile() throws Exception {
        File tmp = File.createTempFile("FileUtilsTest", ".txt");
        tmp.deleteOnExit();
        String testStr = "hello";
        InputStream in = new ByteArrayInputStream(testStr.getBytes());
        FileUtils.writeFile(tmp, in);

        String res = FileUtils.readFile(tmp);
        assertTrue(res.contains("hello"));
    }
}