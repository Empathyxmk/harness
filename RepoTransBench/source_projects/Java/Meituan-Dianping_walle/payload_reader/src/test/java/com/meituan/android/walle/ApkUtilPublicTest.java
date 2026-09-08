package com.meituan.android.walle;

import org.junit.Test;

import java.lang.reflect.Field;

import static org.junit.Assert.*;

public class ApkUtilPublicTest {

    @Test
    public void testApkSigBlockMagicConstants_public() throws Exception {
        // Use reflection to get the constants for extra validation
        Field hi = ApkUtil.class.getDeclaredField("APK_SIG_BLOCK_MAGIC_HI");
        Field lo = ApkUtil.class.getDeclaredField("APK_SIG_BLOCK_MAGIC_LO");

        assertEquals(0x3234206b636f6c42L, hi.get(null));
        assertEquals(0x20676953204b5041L, lo.get(null));
    }

    @Test
    public void testDefaultCharset_public() {
        assertEquals("UTF-8", ApkUtil.DEFAULT_CHARSET);
    }

    @Test
    public void testChannelBlockId_public() {
        assertEquals(0x71777777, ApkUtil.APK_CHANNEL_BLOCK_ID);
    }
}