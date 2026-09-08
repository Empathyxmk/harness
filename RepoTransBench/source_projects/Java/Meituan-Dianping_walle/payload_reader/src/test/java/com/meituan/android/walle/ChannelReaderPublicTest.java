package com.meituan.android.walle;

import org.junit.Test;

import java.io.File;

import static org.junit.Assert.*;

/**
 * Public tests for ChannelReader: test methods with different data focus on
 * null and missing files (since core logic requires valid APKs, which can't be unit tested simply).
 */
public class ChannelReaderPublicTest {

    @Test
    public void testGetChannelByFile_public() {
        File file = new File("nonexistent-public.apk");
        assertNull(ChannelReader.getChannel(file));
    }

    @Test
    public void testGetChannelInfoByFile_public() {
        File file = new File("not-there-and-public.apk");
        assertNull(ChannelReader.getChannelInfo(file));
    }
}