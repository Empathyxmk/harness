// Test shutdown and dummy constructor
package com.jakewharton.picasso;

import org.junit.Test;

public class OkHttp3DownloaderTest {

    @Test
    public void testShutdownDoesNotThrow() {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.shutdown();
        // no asserts, just check no exception
    }

    @Test
    public void testDummyConstructor() {
        OkHttp3Downloader downloader = new OkHttp3Downloader("dummy");
        // no asserts, just check for exceptions
    }
}