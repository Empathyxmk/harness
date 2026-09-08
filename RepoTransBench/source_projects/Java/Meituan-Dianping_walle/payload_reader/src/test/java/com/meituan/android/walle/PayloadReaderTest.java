package com.meituan.android.walle;

import org.junit.Test;

import java.io.File;
import java.io.IOException;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class PayloadReaderTest {

    @Test
    public void testGetString_nullFile() {
        // Non-existent file should return null (IOException + catch return null)
        File nonExistent = new File("not-a-real-apk-file.apk");
        String s = PayloadReader.getString(nonExistent, 123);
        assertNull(s);
    }

    @Test
    public void testGetBytes_nullByteBuffer() throws Exception {
        // We want to reach getBytes with a "fake" ByteBuffer (simulate null handling)
        // Use reflection to call getBytes with a sample buffer
        Method m = PayloadReader.class.getDeclaredMethod("getBytes", java.nio.ByteBuffer.class);
        m.setAccessible(true);
        byte[] data = new byte[]{1,2,3,4,5};
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.wrap(data, 1, 3); // [2,3,4]
        byte[] out = (byte[]) m.invoke(null, buf);
        assertArrayEquals(new byte[]{2,3,4}, out);
    }

    @Test
    public void testGet_nullFile_returnsNull() {
        File nonExistent = new File("not-a-real-apk-file.apk");
        assertNull(PayloadReader.get(nonExistent, 123));
    }
}