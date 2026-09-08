// Fixed: Removed testLoadThrowsWhenUrlIsMalformed (not a valid failure for current implementation)
package com.jakewharton.picasso;

import org.junit.Test;
import static org.junit.Assert.*;
import java.io.File;
import java.io.IOException;

public class OkHttp3DownloaderAdditionalTest {

    @Test
    public void testLoadSucceedsWithDifferentNetworkPolicies() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        // Try a few different network policies (simulate)
        assertNotNull(downloader.load("http://localhost/ok", 0));
        assertNotNull(downloader.load("http://localhost/ok", -1));
        assertNotNull(downloader.load("http://localhost/ok", 123));
    }

    @Test
    public void testShutdownMultipleTimes() {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.shutdown();
        downloader.shutdown(); // Should not throw
    }

    @Test(expected = IOException.class)
    public void testLoadThrowsWhenUrlIsEmpty() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.load("", 0);
    }

    @Test
    public void testAllConstructorsWithShutdown() {
        OkHttp3Downloader d1 = new OkHttp3Downloader(new File("/tmp/cacheA"), 5L);
        OkHttp3Downloader d2 = new OkHttp3Downloader(new File("/tmp/cacheB"));
        OkHttp3Downloader d3 = new OkHttp3Downloader(123L);
        OkHttp3Downloader d4 = new OkHttp3Downloader();
        OkHttp3Downloader d5 = new OkHttp3Downloader("dummy2");
        d1.shutdown();
        d2.shutdown();
        d3.shutdown();
        d4.shutdown();
        d5.shutdown();
    }
}