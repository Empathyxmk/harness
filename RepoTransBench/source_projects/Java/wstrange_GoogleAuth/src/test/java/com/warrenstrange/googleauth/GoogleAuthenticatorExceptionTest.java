package com.warrenstrange.googleauth;

import org.junit.Test;
import static org.junit.Assert.*;

public class GoogleAuthenticatorExceptionTest {

    @Test
    public void testExceptionMessage() {
        GoogleAuthenticatorException ex = new GoogleAuthenticatorException("A message");
        assertEquals("A message", ex.getMessage());
    }

    @Test
    public void testExceptionCause() {
        Throwable cause = new RuntimeException("root");
        GoogleAuthenticatorException ex = new GoogleAuthenticatorException("A message", cause);
        assertEquals("A message", ex.getMessage());
        assertEquals(cause, ex.getCause());
    }
}