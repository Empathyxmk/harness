package com.meituan.android.walle;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;

import java.io.File;

import static org.junit.Assert.*;

public class ApkUtilTest {

    @Rule
    public TemporaryFolder tempFolder = new TemporaryFolder();

    @Test
    public void testGetApkSigningBlock_nullInput() {
        try {
            ApkUtil.getApkSigningBlock(null);
            fail("Should throw NullPointerException");
        } catch (NullPointerException e) {
            // pass
        } catch (Exception e) {
            fail("Unexpected exception: " + e);
        }
    }

    @Test
    public void testGetMapIdValue_emptyArray() {
        assertNull(ApkUtil.getMapIdValue(new ApkUtil.Pair[0], 0L));
    }

    @Test
    public void testFindApkSignatureSchemeV2BlockId() {
        // Since this function requires file, pass a non-existent file to hit IOException
        File dummy = new File("non-existent.apk");
        try {
            ApkUtil.findApkSignatureSchemeV2BlockId(dummy);
            fail("Should throw Exception");
        } catch (Exception e) {
            // Expected: because the file doesn't exist
            assertTrue(e instanceof java.io.IOException);
        }
    }

}