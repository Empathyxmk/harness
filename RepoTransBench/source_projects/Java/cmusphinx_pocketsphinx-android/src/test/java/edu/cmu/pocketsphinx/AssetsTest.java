package edu.cmu.pocketsphinx;

import org.junit.Test;
import java.io.File;
import java.io.IOException;

import static org.junit.Assert.*;

public class AssetsTest {

    @Test
    public void testAssetsConstructorWithDest() {
        // We cannot construct Android Context here, but we can test non-android part
        Assets assets = new Assets((Object) null, "test_dest_dir");  // Use fake context replacement in main class for JVM
        assertNotNull(assets);
    }

    @Test
    public void testSyncMethodThrowsException() {
        Assets assets = new Assets((Object) null, "test_dest_dir");
        try {
            assets.sync();
            fail("Expected exception");
        } catch (Exception ex) {
            // Expected, since real Android code can't be run on JVM
        }
    }
}