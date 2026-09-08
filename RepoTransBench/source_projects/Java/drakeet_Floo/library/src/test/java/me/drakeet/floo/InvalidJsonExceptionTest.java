package me.drakeet.floo;

import org.junit.Test;

public class InvalidJsonExceptionTest {

    @Test
    public void testConstructorWithMessageAndThrowable() {
        Throwable t = new RuntimeException("test");
        InvalidJsonException ex = new InvalidJsonException("message", t);
        assert ex.getMessage().contains("message");
        assert ex.getCause() == t;
    }
}