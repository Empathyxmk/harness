package com.example.public_tests;

import com.example.txweb.Error;
import com.example.txweb.Handler;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class PublicTxwebTest {

    @Test
    void testPublicErrorProperties() {
        Error err = new Error(1000, "unknown error", java.util.Map.of("prop", "value"));
        assertEquals(1000, err.code);
        assertEquals("unknown error", err.message);
        assertEquals(java.util.Map.of("prop", "value"), err.data);
    }

    @Test
    void testPublicErrorStrRepr() {
        Error err = new Error(404, "resource not here");
        assertEquals("resource not here", err.toString());
        assertEquals("Error(404, 'resource not here')", err.repr());
    }

    @Test
    void testPublicHandlerReturnsNotFound() {
        class DummyHandler extends Handler {
            public Object call(Object... args) {
                throw new Error(404, "Not Found");
            }
        }
        Handler handler = new DummyHandler();
        try {
            handler.call();
            fail();
        } catch (Error e) {
            assertEquals(404, e.code);
            assertEquals("Not Found", e.message);
        }
    }
}