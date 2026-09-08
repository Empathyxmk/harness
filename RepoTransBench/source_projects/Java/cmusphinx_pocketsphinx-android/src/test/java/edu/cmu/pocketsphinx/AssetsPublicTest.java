package edu.cmu.pocketsphinx;

import org.junit.Test;
import static org.junit.Assert.*;

public class AssetsPublicTest {

    @Test
    public void testAssetsConstructorWithDifferentDest() {
        Assets assets = new Assets((Object) null, "public_dest_dir_v2");
        assertNotNull(assets);
    }

    @Test
    public void testSyncMethodThrowsExceptionWithPublicData() {
        Assets assets = new Assets((Object) null, "public_dest_dir_v2");
        try {
            assets.sync();
            fail("Expected exception");
        } catch (Exception ex) {
            // Expected, but different dest tested here
        }
    }
}