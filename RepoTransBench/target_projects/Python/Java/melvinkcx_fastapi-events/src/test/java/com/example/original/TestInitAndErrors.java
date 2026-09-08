package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestInitAndErrors {
    @Test
    void testErrorClassMessage() {
        SomeError err = new SomeError("foo!");
        assertEquals("foo!", err.getMessage());
    }

    @Test
    void testClassNotPresentThrows() {
        Exception ex = assertThrows(ClassNotFoundException.class, () -> Class.forName("not.present.Clazz"));
        assertNotNull(ex);
    }

    private static class SomeError extends Exception {
        SomeError(String msg) { super(msg); }
    }
}