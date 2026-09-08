package com.overholt.original;

import com.overholt.wsgi.Wsgi;
import com.overholt.wsgi.AppApplication;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class WsgiTest {

    @Test
    void testWsgiApplicationExists() {
        assertNotNull(Wsgi.application);
    }

    @Test
    void testWsgiMainRunSimple() {
        String result = Wsgi.runSimple("localhost", 8080, Wsgi.application, false, false);
        assertEquals("ran", result);
        assertNotNull(Wsgi.application);
    }
}