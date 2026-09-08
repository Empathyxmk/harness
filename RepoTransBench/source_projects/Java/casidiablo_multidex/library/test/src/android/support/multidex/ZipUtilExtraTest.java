package android.support.multidex;

import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.io.RandomAccessFile;
import java.util.zip.ZipException;

import static org.junit.Assert.*;

public class ZipUtilExtraTest {

    @Test(expected = ZipException.class)
    public void testFindCentralDirectoryShortFile() throws IOException {
        File f = File.createTempFile("shortzip", ".zip");
        try (RandomAccessFile raf = new RandomAccessFile(f, "rw")) {
            raf.setLength(1); // deliberately too short
            ZipUtil.findCentralDirectory(raf);
        } finally {
            f.delete();
        }
    }
}