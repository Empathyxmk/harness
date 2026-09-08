package com.jakewharton.picasso;

import org.junit.Test;

public class OkHttp3DownloaderPublicTest {

    @Test
    public void testShutdownIsSafeRepeatedly() {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.shutdown();
        downloader.shutdown();
        // Still no exception
    }

    @Test
    public void testAnotherDummyConstructor() {
        OkHttp3Downloader downloader = new OkHttp3Downloader("publicValue");
    }
}