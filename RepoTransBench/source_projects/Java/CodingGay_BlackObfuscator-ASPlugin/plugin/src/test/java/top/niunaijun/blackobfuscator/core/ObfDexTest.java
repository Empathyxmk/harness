package top.niunaijun.blackobfuscator.core;

import org.junit.Test;
import java.io.*;

public class ObfDexTest {
    @Test
    public void testObfNonExistentDir() {
        // Should not throw, input dir does not exist
        ObfDex.obf("not/a/real/directory", 1, new String[0], new String[0], null);
    }

    @Test
    public void testObfSingleFileThatIsNotDex() throws IOException {
        File tmp = File.createTempFile("notadex", ".txt");
        try {
            ObfDex.obf(tmp.getAbsolutePath(), 1, new String[0], new String[0], null);
        } finally {
            tmp.delete();
        }
    }

    @Test
    public void testObfEmptyDirectory() throws IOException {
        File dir = new File(System.getProperty("java.io.tmpdir"), "empty_dir_for_obf_test_"+System.nanoTime());
        dir.mkdir();
        try {
            ObfDex.obf(dir.getAbsolutePath(), 1, new String[0], new String[0], null);
        } finally {
            dir.delete();
        }
    }
}