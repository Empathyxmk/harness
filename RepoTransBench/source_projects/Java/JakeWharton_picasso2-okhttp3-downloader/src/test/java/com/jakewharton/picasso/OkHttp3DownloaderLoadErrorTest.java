// Minimal test class without external dependencies or mock servers
package com.jakewharton.picasso;

import org.junit.Test;
import static org.junit.Assert.*;

import java.io.IOException;

public class OkHttp3DownloaderLoadErrorTest {

    @Test(expected = IOException.class)
    public void testLoadThrowsOnNullUrl() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.load(null, 0);
    }

    @Test(expected = IOException.class)
    public void testLoadThrowsOnInvalidUrl() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.load("ftp://localhost/abc", 0);
    }

    @Test
    public void testLoadSucceedsOnValidUrl() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        Object result = downloader.load("http://localhost/abc", 0);
        assertNotNull(result);
    }
}