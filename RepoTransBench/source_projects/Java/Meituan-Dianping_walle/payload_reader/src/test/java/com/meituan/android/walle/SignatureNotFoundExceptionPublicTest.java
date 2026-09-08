package com.meituan.android.walle;

import org.junit.Test;

import static org.junit.Assert.*;

public class SignatureNotFoundExceptionPublicTest {

    @Test
    public void testConstructorMessage_public() {
        SignatureNotFoundException ex = new SignatureNotFoundException("another message");
        assertEquals("another message", ex.getMessage());
        assertNull(ex.getCause());
    }

    @Test
    public void testConstructorMessageAndCause_public() {
        Throwable cause = new NullPointerException("public cause");
        SignatureNotFoundException ex = new SignatureNotFoundException("public error", cause);
        assertEquals("public error", ex.getMessage());
        assertEquals(cause, ex.getCause());
    }
}