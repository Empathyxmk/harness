package io.paperdb;

import org.junit.Test;

import static org.junit.Assert.*;

public class PaperDbExceptionPublicTest {

    @Test
    public void testMessageConstructor_public() {
        PaperDbException ex = new PaperDbException("fail-public");
        assertEquals("fail-public", ex.getMessage());
    }

    @Test
    public void testMessageAndThrowableConstructor_public() {
        Throwable t = new Exception("public-cause");
        PaperDbException ex = new PaperDbException("fail-public2", t);
        assertEquals("fail-public2", ex.getMessage());
        assertEquals(t, ex.getCause());
    }
}