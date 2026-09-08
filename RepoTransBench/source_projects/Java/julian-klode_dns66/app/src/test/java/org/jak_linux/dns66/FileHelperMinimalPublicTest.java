package org.jak_linux.dns66;

import org.junit.Test;

import java.io.IOException;
import java.io.StringWriter;
import java.util.concurrent.atomic.AtomicReference;

import static org.junit.Assert.*;

public class FileHelperMinimalPublicTest {
    @Test
    public void testCloseOrWarnNoThrow() {
        StringWriter writer = new StringWriter();
        FileHelper.closeOrWarn(writer, "publicTest", "nothing should fail here");
        // Writer is still valid for writing after closeOrWarn, as StringWriter.close() is non-op
        writer.write("hello world");
        assertEquals("hello world", writer.toString());
    }

    @Test
    public void testCloseOrWarnWithException() {
        AtomicReference<Boolean> closed = new AtomicReference<>(false);
        java.io.Writer badWriter = new java.io.StringWriter() {
            @Override
            public void close() throws IOException {
                closed.set(true);
                throw new IOException("public test error");
            }
        };
        FileHelper.closeOrWarn(badWriter, "tag", "public test warn");
        assertTrue(closed.get());
    }
}