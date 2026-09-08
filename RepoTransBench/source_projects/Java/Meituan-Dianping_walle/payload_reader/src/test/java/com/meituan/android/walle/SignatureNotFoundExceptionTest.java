package com.meituan.android.walle;

import org.junit.Test;

import static org.junit.Assert.*;

public class SignatureNotFoundExceptionTest {

    @Test
    public void testConstructorMessage() {
        SignatureNotFoundException ex = new SignatureNotFoundException("test message");
        assertEquals("test message", ex.getMessage());
        assertNull(ex.getCause());
    }

    @Test
    public void testConstructorMessageAndCause() {
        Throwable cause = new RuntimeException("cause");
        SignatureNotFoundException ex = new SignatureNotFoundException("err", cause);
        assertEquals("err", ex.getMessage());
        assertEquals(cause, ex.getCause());
    }
}