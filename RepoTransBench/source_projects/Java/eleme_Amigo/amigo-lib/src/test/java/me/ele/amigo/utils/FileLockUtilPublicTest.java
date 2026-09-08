package me.ele.amigo.utils;

import org.junit.Test;
import java.io.File;
import java.io.RandomAccessFile;
import static org.junit.Assert.*;

public class FileLockUtilPublicTest {

    @Test
    public void publicTestLockUnlockFileDiff() throws Exception {
        // Use a different temp file for public
        File file = File.createTempFile("public_testfile_lock", ".tmp");
        RandomAccessFile raf = new RandomAccessFile(file, "rw");
        try {
            long pos = 2;
            long size = 7;
            assertNotNull(FileLockUtil.lock(raf.getChannel(), pos, size));
            FileLockUtil.unlock(raf.getChannel()); // should not throw
        } finally {
            raf.close();
            file.delete();
        }
    }
}