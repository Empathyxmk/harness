package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class InvalidJsonExceptionPublicTest {

    @Test
    public void testMessage_public() {
        InvalidJsonException e = new InvalidJsonException("New message for public test");
        assertEquals("New message for public test", e.getMessage());
    }

    @Test
    public void testNullMessage_public() {
        InvalidJsonException e = new InvalidJsonException(null);
        assertNull(e.getMessage());
    }
}