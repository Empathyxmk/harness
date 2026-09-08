package org.jak_linux.dns66;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;

public class FileHelperPublicTest {

    private File file;

    @Before
    public void setUp() throws Exception {
        file = File.createTempFile("dns66test_public_", ".txt");
        file.deleteOnExit();
    }

    @After
    public void tearDown() {
        file.delete();
    }

    @Test
    public void testReadFileAndWriteFilePublic() throws Exception {
        OutputStream out = new FileOutputStream(file);
        out.write("public file test data".getBytes());
        out.close();

        String content = FileHelper.readFile(file);
        assertEquals("public file test data", content);

        File otherFile = File.createTempFile("dns66test_public_other_", ".txt");
        FileHelper.writeFile(otherFile, "abc_public");
        String secondRead = FileHelper.readFile(otherFile);
        assertEquals("abc_public", secondRead);
        otherFile.delete();
    }

    @Test(expected = IOException.class)
    public void testReadFileThrowsPublic() throws Exception {
        File notAFile = new File(file.getAbsolutePath() + "_notfound_public");
        FileHelper.readFile(notAFile);
    }
}