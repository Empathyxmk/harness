// Ensure default constructor does not throw
package com.jakewharton.picasso;

import org.junit.Test;

public class OkHttp3DownloaderCtorTest {

    @Test
    public void testNoArgCtor() {
        OkHttp3Downloader downloader = new OkHttp3Downloader();
        // no asserts, just check for exceptions
    }
}