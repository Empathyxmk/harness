package com.tiddl.original;

import org.junit.jupiter.api.*;

import static org.junit.jupiter.api.Assertions.*;

class ExceptionsUnitTest {
    static class MyException extends Exception {
        int code;
        String msg;
        MyException(int code, String msg) { this.code = code; this.msg = msg; }
        @Override
        public String getMessage() { return msg; }
    }
    static class AnotherException extends Exception {
        AnotherException(String m) { super(m); }
    }
    @Test
    void test_my_exception_fields() {
        MyException ex = new MyException(404, "Not Found");
        assertEquals(404, ex.code);
        assertEquals("Not Found", ex.getMessage());
    }
    @Test
    void test_my_exception_throws() {
        Exception ex = assertThrows(MyException.class, () -> { throw new MyException(400, "Oops"); });
        assertTrue(ex.getMessage().contains("Oops"));
    }
    @Test
    void test_another_exception_message() {
        Exception ex = assertThrows(AnotherException.class, () -> { throw new AnotherException("fail"); });
        assertEquals("fail", ex.getMessage());
    }
}