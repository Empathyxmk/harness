package com.jakewharton.picasso;

import org.junit.Test;
import java.io.IOException;

public class OkHttp3DownloaderLoadErrorPublicTest {

    @Test(expected = IOException.class)
    public void testLoadThrowsOnInvalidProtocol() throws IOException {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        downloader.load("ftp://someurl", 0); // Should throw, not 'http'
    }
}