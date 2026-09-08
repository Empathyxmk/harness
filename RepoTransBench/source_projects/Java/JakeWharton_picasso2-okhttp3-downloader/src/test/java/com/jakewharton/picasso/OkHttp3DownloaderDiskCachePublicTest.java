package com.jakewharton.picasso;

import org.junit.Test;

import java.io.File;

public class OkHttp3DownloaderDiskCachePublicTest {

    @Test
    public void testCtorWithAnotherCacheDir() {
        File file = new File("/tmp/pub_cache_c");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file);
    }

    @Test
    public void testCtorWithAnotherCacheDirAndMaxSize() {
        File file = new File("/tmp/pub_cache_d");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file, 5555L);
    }

    @Test
    public void testCtorWithAnotherMaxSize() {
        OkHttp3Downloader downloader = new OkHttp3Downloader(9876L);
    }
}