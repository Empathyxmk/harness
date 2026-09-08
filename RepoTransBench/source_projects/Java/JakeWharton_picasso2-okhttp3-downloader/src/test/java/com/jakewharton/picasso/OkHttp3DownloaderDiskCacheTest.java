// Minimal test for constructors relating to cacheDir and maxSize—no real disk/cache logic
package com.jakewharton.picasso;

import org.junit.Test;

import java.io.File;

public class OkHttp3DownloaderDiskCacheTest {

    @Test
    public void testCtorWithCacheDir() {
        File file = new File("/tmp/cache");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file);
        // no asserts, just check for exceptions
    }

    @Test
    public void testCtorWithCacheDirAndMaxSize() {
        File file = new File("/tmp/cache");
        OkHttp3Downloader downloader = new OkHttp3Downloader(file, 1024L);
        // no asserts, just check for exceptions
    }

    @Test
    public void testCtorWithMaxSize() {
        OkHttp3Downloader downloader = new OkHttp3Downloader(4096L);
        // no asserts, just check for exceptions
    }
}