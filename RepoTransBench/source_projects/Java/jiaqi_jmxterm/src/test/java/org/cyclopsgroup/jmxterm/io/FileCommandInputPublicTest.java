package org.cyclopsgroup.jmxterm.io;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;

public class FileCommandInputPublicTest {

    private File tempFile;

    @Before
    public void setUp() throws IOException {
        tempFile = File.createTempFile("publictestinput", ".tmp");
        try (FileWriter fw = new FileWriter(tempFile)) {
            fw.write("Alpha\nBeta\nGamma\n");
        }
    }

    @After
    public void tearDown() {
        if (tempFile != null) {
            tempFile.delete();
        }
    }

    @Test
    public void testReadLinesFromFile() throws IOException {
        FileCommandInput input = new FileCommandInput(tempFile.getAbsolutePath());
        assertEquals("Alpha", input.readLine());
        assertEquals("Beta", input.readLine());
        assertEquals("Gamma", input.readLine());
        assertNull("Should return null at end of file", input.readLine());
        input.close();
    }
}