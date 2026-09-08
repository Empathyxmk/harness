package org.csource.fastdfs;

import org.junit.Test;

import static org.junit.Assert.*;

public class DownloadCallbackPublicTest {

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
    public void testCallbackPublic() {
        TestDownloadCallback cb = new TestDownloadCallback();
        byte[] data = {10, 20, 30, 40, 50};
        int bytes = cb.recv(987654321L, data, data.length);
        assertEquals(0, bytes);
        assertEquals(987654321L, cb.lastFileSize);
        assertArrayEquals(data, cb.lastData);
        assertEquals(data.length, cb.lastBytes);
    }
}