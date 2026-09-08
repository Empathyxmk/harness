package com.cloudconvert.original;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class ExceptionsTest {

    static class ApiError extends Exception {
        int code;
        ApiError(String msg, int code) { super(msg); this.code = code; }
    }
    static class TimeoutException extends Exception { TimeoutException(String m) { super(m); } }
    static class AuthException extends Exception { AuthException(String m) { super(m); } }
    static class ParseException extends Exception { ParseException(String m) { super(m); } }
    static class InvalidRequest extends Exception { InvalidRequest(String m) { super(m); } }
    static class InvalidResponse extends Exception { InvalidResponse(String m) { super(m); } }
    static class ConnectionFailed extends Exception { ConnectionFailed(String m) { super(m); } }

    @Test
    void testApiErrorStr() throws ApiError {
        ApiError e = new ApiError("msg", 400);
        assertTrue(e.getMessage().contains("msg"));
        assertEquals(400, e.code);
    }

    @Test
    void testTimeoutException() {
        TimeoutException e = new TimeoutException("Timeouted!");
        assertTrue(e instanceof TimeoutException);
        assertEquals("Timeouted!", e.getMessage());
    }

    @Test
    void testAuthException() {
        AuthException e = new AuthException("Unauthorized");
        assertTrue(e instanceof AuthException);
        assertEquals("Unauthorized", e.getMessage());
    }

    @Test
    void testParseException() {
        ParseException e = new ParseException("bad parse");
        assertTrue(e instanceof ParseException);
        assertEquals("bad parse", e.getMessage());
    }

    @Test
    void testInvalidRequest() {
        InvalidRequest e = new InvalidRequest("invalid");
        assertTrue(e instanceof InvalidRequest);
        assertEquals("invalid", e.getMessage());
    }

    @Test
    void testInvalidResponse() {
        InvalidResponse e = new InvalidResponse("invalidresp");
        assertTrue(e instanceof InvalidResponse);
        assertEquals("invalidresp", e.getMessage());
    }

    @Test
    void testConnectionFailed() {
        ConnectionFailed e = new ConnectionFailed("fail");
        assertTrue(e instanceof ConnectionFailed);
        assertEquals("fail", e.getMessage());
    }
}