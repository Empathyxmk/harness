package org.jak_linux.dns66;

import org.junit.After;
import org.junit.Before;
import org.junit.Test;

import java.io.*;

import static org.junit.Assert.*;

public class SingleWriterMultipleReaderFilePublicTest {

    private File file;
    private SingleWriterMultipleReaderFile sfile;

    @Before
    public void setUp() throws Exception {
        file = File.createTempFile("swmr_public_", ".txt");
        file.deleteOnExit();
        sfile = new SingleWriterMultipleReaderFile(file);
    }

    @After
    public void tearDown() {
        file.delete();
        // Remove the work file if present
        File work = new File(file.getAbsolutePath() + ".dns66-new");
        work.delete();
    }

    @Test
    public void testStartFinishWritePublic() throws Exception {
        FileOutputStream fos = sfile.startWrite();
        fos.write("abc_public".getBytes());
        sfile.finishWrite(fos);

        InputStream in = sfile.openRead();
        byte[] buf = new byte[20];
        int n = in.read(buf);
        String got = new String(buf, 0, n);
        in.close();
        assertEquals("abc_public", got);
    }

    @Test(expected = FileNotFoundException.class)
    public void testOpenReadFileNotFoundPublic() throws Exception {
        File tmp = new File(file.getAbsolutePath() + "_new_public");
        SingleWriterMultipleReaderFile sf = new SingleWriterMultipleReaderFile(tmp);
        sf.openRead();
    }
}