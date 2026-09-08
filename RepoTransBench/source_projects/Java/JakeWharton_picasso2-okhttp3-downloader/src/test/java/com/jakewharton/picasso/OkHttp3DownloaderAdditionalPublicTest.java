package com.jakewharton.picasso;

import org.junit.Test;
import static org.junit.Assert.*;
import java.io.File;
import java.io.IOException;

public class OkHttp3DownloaderAdditionalPublicTest {

    @Test
    public void testLoadSucceedsWithOtherNetworkPolicies() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        // Use a different URL path and network policies
        assertNotNull(downloader.load("http://127.0.0.1/success", 1));
        assertNotNull(downloader.load("http://127.0.0.1/success", 42));
        assertNotNull(downloader.load("http://127.0.0.1/success", -100));
    }

    @Test
    public void testShutdownManyTimes() {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.shutdown();
        downloader.shutdown();
        downloader.shutdown(); // Should not throw, extra shutdown
    }

    @Test(expected = IOException.class)
    public void testLoadThrowsWhenUrlIsNullString() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.load(null, 0);
    }

    @Test
    public void testAllConstructorsWithShutdownPublic() {
        OkHttp3Downloader d1 = new OkHttp3Downloader(new File("/tmp/pub_cacheA"), 15L);
        OkHttp3Downloader d2 = new OkHttp3Downloader(new File("/tmp/pub_cacheB"));
        OkHttp3Downloader d3 = new OkHttp3Downloader(321L);
        OkHttp3Downloader d4 = new OkHttp3Downloader();
        OkHttp3Downloader d5 = new OkHttp3Downloader("publicDummy");
        d1.shutdown();
        d2.shutdown();
        d3.shutdown();
        d4.shutdown();
        d5.shutdown();
    }
}