package com.tiddl.public_tests;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class PublicExceptionsUnitTest {

    static class PublicException extends Exception {
        int code;
        String msg;
        PublicException(int code, String msg) { this.code = code; this.msg = msg; }
        @Override
        public String getMessage() { return msg; }
    }

    @Test
    void test_public_exception_fields() {
        PublicException ex = new PublicException(404, "Not Found");
        assertEquals(404, ex.code);
        assertEquals("Not Found", ex.getMessage());
    }

    @Test
    void test_public_exception_throws() {
        Exception ex = assertThrows(PublicException.class, () -> {
            throw new PublicException(400, "Oops");
        });
        assertTrue(ex.getMessage().contains("Oops"));
    }
}