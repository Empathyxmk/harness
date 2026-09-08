// Minimal stub for non-Android test and coverage purposes
package com.jakewharton.picasso;

import java.io.File;
import java.io.IOException;

public class OkHttp3Downloader {

    public OkHttp3Downloader(File cacheDir, long maxSize) {
        // Simulate cache directory + max size constructor
    }

    public OkHttp3Downloader(File cacheDir) {
        // Simulate cache directory only constructor
    }

    public OkHttp3Downloader(long maxSize) {
        // Simulate maxSize only constructor
    }

    public OkHttp3Downloader() {
        // No-arg constructor
    }

    public OkHttp3Downloader(String dummy) {
        // Dummy for test stubbing
    }

    public void shutdown() {
        // Simulate resource shutdown
    }

    public Object load(String url, int networkPolicy) throws IOException {
        if (url == null || !url.startsWith("http")) {
            throw new IOException("Invalid URL");
        }
        // Simulate a successful load
        return new Object();
    }
}