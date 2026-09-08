package com.overholt.publictests;

import com.overholt.wsgi.Wsgi;
import com.overholt.wsgi.AppApplication;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicWsgiTest {

    @Test
    void testPublicWsgiApplicationType() {
        // In Python: isinstance(wsgi.application, DispatcherMiddleware)
        // Here: AppApplication
        assertTrue(Wsgi.application instanceof AppApplication);
    }

    @Test
    void testPublicWsgiApplicationMapping() {
        assertTrue(Wsgi.application.getMounts().containsKey("/api"));
    }
}