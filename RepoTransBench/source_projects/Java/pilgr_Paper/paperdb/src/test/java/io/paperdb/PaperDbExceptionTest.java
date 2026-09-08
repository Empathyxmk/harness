package io.paperdb;

import org.junit.Test;

import static org.junit.Assert.*;

public class PaperDbExceptionTest {

    @Test
    public void testMessageConstructor() {
        PaperDbException ex = new PaperDbException("fail");
        assertEquals("fail", ex.getMessage());
    }

    @Test
    public void testMessageAndThrowableConstructor() {
        Throwable t = new Exception("t cause");
        PaperDbException ex = new PaperDbException("fail2", t);
        assertEquals("fail2", ex.getMessage());
        assertEquals(t, ex.getCause());
    }
}