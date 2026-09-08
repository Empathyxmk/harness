package org.csource.fastdfs;

import org.junit.Test;

import static org.junit.Assert.*;

public class DownloadCallbackTest {

    private static class TestDownloadCallback implements DownloadCallback {
        public int lastBytes;
        public long lastFileSize;
        public byte[] lastData;

        @Override
        public int recv(long file_size, byte[] data, int bytes) {
            this.lastFileSize = file_size;
            this.lastData = data;
            this.lastBytes = bytes;
            return 0;
        }
    }

    @Test
    public void testRecv() {
        TestDownloadCallback callback = new TestDownloadCallback();
        byte[] data = new byte[] {1, 2, 3};
        int result = callback.recv(123L, data, data.length);

        assertEquals(0, result);
        assertEquals(123L, callback.lastFileSize);
        assertArrayEquals(data, callback.lastData);
        assertEquals(data.length, callback.lastBytes);
    }
}