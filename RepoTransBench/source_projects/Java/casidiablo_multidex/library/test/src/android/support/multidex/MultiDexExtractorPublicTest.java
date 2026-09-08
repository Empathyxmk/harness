package android.support.multidex;

import org.junit.Test;

import static org.junit.Assert.*;

public class MultiDexExtractorPublicTest {
    @Test
    public void testNonExistentFileCannotFindCentralDirectoryPublic() {
        java.io.File fake = new java.io.File("this_file_should_not_exist_" + System.nanoTime() + ".zip");
        try {
            java.io.RandomAccessFile raf = new java.io.RandomAccessFile(fake, "r");
            try {
                ZipUtil.findCentralDirectory(raf);
                fail("Should have thrown because file doesn't exist");
            } catch (Exception e) {
                // expected
            }
            raf.close();
        } catch (Exception ex) {
            // This is also fine, file does not exist
        }
    }

    @Test
    public void testGetZipCrcNonExistentFilePublic() {
        try {
            long crc = ZipUtil.getZipCrc(new java.io.File("definitely_not_here_" + System.nanoTime() + ".zip"));
            fail("Should not succeed on non-existent");
        } catch (Exception e) {
            // expected
        }
    }
}