package com.example.jsonrpc.original;

import com.example.jsonrpc.manager.SessionManager;
import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

class TestManager {

    @Test
    void testSessionCreateAndGet() {
        SessionManager manager = new SessionManager();
        String sessionId = manager.createSession();
        assertNotNull(sessionId);

        assertNotNull(manager.getSession(sessionId));
    }

    @Test
    void testSessionNotFound() {
        SessionManager manager = new SessionManager();
        assertNull(manager.getSession("not-exist"));
    }
}