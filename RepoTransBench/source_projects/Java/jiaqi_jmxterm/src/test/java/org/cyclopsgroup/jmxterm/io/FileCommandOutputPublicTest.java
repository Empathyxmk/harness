package org.cyclopsgroup.jmxterm.io;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;

public class FileCommandOutputPublicTest {

    private File tempFile;

    @Before
    public void setUp() throws IOException {
        tempFile = File.createTempFile("publictestoutput", ".tmp");
    }

    @After
    public void tearDown() {
        if (tempFile != null) {
            tempFile.delete();
        }
    }

    @Test
    public void testWriteToFile() throws IOException {
        FileCommandOutput output = new FileCommandOutput(tempFile.getAbsolutePath());
        output.print("PublicTest Output Line");
        output.println(" 12345");
        output.flush();
        output.close();

        try (BufferedReader reader = new BufferedReader(new FileReader(tempFile))) {
            String content = reader.readLine();
            assertTrue(content.contains("PublicTest Output Line"));
            String secondLine = reader.readLine();
            assertTrue(secondLine.contains("12345"));
        }
    }
}