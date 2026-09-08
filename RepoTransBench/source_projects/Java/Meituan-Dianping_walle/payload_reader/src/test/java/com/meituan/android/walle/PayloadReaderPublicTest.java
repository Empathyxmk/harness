package com.meituan.android.walle;

import org.junit.Test;

import java.io.File;
import java.lang.reflect.Method;

import static org.junit.Assert.*;

public class PayloadReaderPublicTest {

    @Test
    public void testGetString_nullFile_public() {
        // Use a different non-existent file name
        File nonExistent = new File("definitely-not-an-apk-file-public.apk");
        String s = PayloadReader.getString(nonExistent, 888888);
        assertNull(s);
    }

    @Test
    public void testGetBytes_differentByteBuffer() throws Exception {
        // Use a different buffer sequence and offset
        Method m = PayloadReader.class.getDeclaredMethod("getBytes", java.nio.ByteBuffer.class);
        m.setAccessible(true);
        byte[] data = new byte[]{10,20,30,40,50,60};
        java.nio.ByteBuffer buf = java.nio.ByteBuffer.wrap(data, 2, 2); // [30,40]
        byte[] out = (byte[]) m.invoke(null, buf);
        assertArrayEquals(new byte[]{30,40}, out);
    }

    @Test
    public void testGet_nullFile_returnsNull_public() {
        File nonExistent = new File("another-fake-apk-file-public.apk");
        assertNull(PayloadReader.get(nonExistent, 999999));
    }
}