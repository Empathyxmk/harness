package com.jakewharton.picasso;

import org.junit.Test;

import java.io.File;

public class OkHttp3DownloaderCtorPublicTest {

    @Test
    public void testPublicCtorWithCacheDir() {
        File file = new File("/tmp/public_ctor_cache");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file);
        // Only for exception check
    }

    @Test
    public void testPublicCtorWithCacheDirAndMaxSize() {
        File file = new File("/tmp/public_ctor_cache2");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file, 2048L);
        // Only for exception check
    }

    @Test
    public void testPublicCtorWithMaxSize() {
        OkHttp3Downloader downloader = new OkHttp3Downloader(8192L);
        // Only for exception check
    }
}