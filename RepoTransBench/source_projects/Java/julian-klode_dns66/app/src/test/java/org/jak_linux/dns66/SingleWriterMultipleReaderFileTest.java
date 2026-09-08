package org.jak_linux.dns66;

import org.junit.*;
import java.io.*;

public class SingleWriterMultipleReaderFileTest {

    private File tempDir;
    private File activeFile;
    private SingleWriterMultipleReaderFile file;

    @Before
    public void setUp() throws Exception {
        tempDir = new File(System.getProperty("java.io.tmpdir"), "swmrf_tests_" + System.nanoTime());
        tempDir.mkdir();
        activeFile = new File(tempDir, "testfile.txt");
        file = new SingleWriterMultipleReaderFile(activeFile);
    }

    @After
    public void tearDown() {
        if (activeFile.exists()) activeFile.delete();
        File workFile = new File(activeFile.getAbsolutePath() + ".dns66-new");
        if (workFile.exists()) workFile.delete();
        tempDir.delete();
    }

    @Test
    public void testWriteAndRead() throws Exception {
        String content = "hello world";
        FileOutputStream out = file.startWrite();
        out.write(content.getBytes());
        file.finishWrite(out);

        InputStream in = file.openRead();
        byte[] buf = new byte[content.length()];
        in.read(buf);
        in.close();
        Assert.assertEquals(content, new String(buf));
    }

    @Test(expected = FileNotFoundException.class)
    public void testReadNonExistentFile() throws Exception {
        SingleWriterMultipleReaderFile f = new SingleWriterMultipleReaderFile(new File(tempDir, "nonexistent.txt"));
        f.openRead();
    }

    @Test
    public void testFailWrite() throws Exception {
        FileOutputStream out = file.startWrite();
        out.write("data".getBytes());
        // purposely close underlying file so finishWrite throws
        out.close();
        // work file exists but finishWrite fails
        try {
            file.finishWrite(out);
            Assert.fail();
        } catch (IOException e) {
            // expected
        }
        // Make sure work file is deleted after failWrite
        Assert.assertFalse(new File(activeFile.getAbsolutePath() + ".dns66-new").exists());
    }

    @Test
    public void testWorkFileDeletionFailure() throws Exception {
        FileOutputStream out = file.startWrite();
        out.close();
        // create work file and make it non-deletable
        File workFile = new File(activeFile.getAbsolutePath() + ".dns66-new");
        workFile.createNewFile();
        workFile.setWritable(false);

        try {
            file.failWrite(new FileOutputStream(workFile));
            Assert.fail();
        } catch (IOException e) {
            // Expected: cannot delete
        } finally {
            workFile.setWritable(true);
            workFile.delete();
        }
    }
}