package net.redwarp.tool.resizer;

import org.junit.*;
import java.io.*;

public class FileToolsPublicTest {

    private File tempInput;
    private File tempOutput;

    @Before
    public void setUp() throws IOException {
        tempInput = File.createTempFile("pinput", ".dat");
        tempOutput = File.createTempFile("poutput", ".dat");
        // Write different data to input file
        try (FileWriter writer = new FileWriter(tempInput)) {
            writer.write("Public Test Data!!");
        }
        tempOutput.delete(); // so FileTools.copyfile can create it
    }

    @After
    public void tearDown() {
        if (tempInput != null) tempInput.delete();
        if (tempOutput != null) tempOutput.delete();
    }

    @Test
    public void testCopyFileNormal() throws Exception {
        FileTools.copyfile(tempInput, tempOutput);
        Assert.assertTrue(tempOutput.exists());
        String content = "";
        try (BufferedReader reader = new BufferedReader(new FileReader(tempOutput))) {
            content = reader.readLine();
        }
        Assert.assertEquals("Public Test Data!!", content);
    }

    @Test
    public void testCopyFileInputFileNotExist() {
        File input = new File("missing_file_abc123.txt");
        // System.exit(0) will kill the JVM, so expect a SecurityException
        SecurityManager original = System.getSecurityManager();
        System.setSecurityManager(new NoExitSecurityManager());
        try {
            FileTools.copyfile(input, tempOutput);
            Assert.fail("Expected SecurityException");
        } catch (SecurityException ex) {
            // expected
        } finally {
            System.setSecurityManager(original);
        }
    }

    @Test
    public void testCopyFileIOException() throws Exception {
        // Output is a folder, triggers IOException
        File folder = File.createTempFile("pfolder", "");
        folder.delete();
        folder.mkdir();
        try {
            FileTools.copyfile(tempInput, folder);
            Assert.assertTrue(folder.isDirectory());
        } finally {
            folder.delete();
        }
    }

    // Custom SecurityManager to intercept System.exit
    static class NoExitSecurityManager extends SecurityManager {
        @Override public void checkPermission(java.security.Permission perm) { }
        @Override public void checkExit(int status) { throw new SecurityException(); }
    }
}