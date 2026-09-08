package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicExceptionsTest {

    static class ApiError extends Exception {
        ApiError(String m) { super(m); }
    }
    static class TimeoutException extends Exception { TimeoutException(String m) { super(m); } }

    @Test
    void testApiError() throws ApiError {
        ApiError e = new ApiError("fail");
        assertEquals("fail", e.getMessage());
    }
    @Test
    void testTimeoutException() {
        TimeoutException e = new TimeoutException("timeout!");
        assertEquals("timeout!", e.getMessage());
        assertTrue(e instanceof TimeoutException);
    }
}