package com.sshaudit.original;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

public class TestErrors {

    public static class SshAuditError extends Exception {
        public SshAuditError(String msg) {
            super(msg);
        }
    }

    public static class AuthError extends SshAuditError {
        public AuthError(String msg) { super(msg); }
    }
    public static class ConnectionError extends SshAuditError {
        public ConnectionError(String msg) { super(msg); }
    }
    public static class ProtocolError extends SshAuditError {
        public ProtocolError(String msg) { super(msg); }
    }

    @Test
    public void test_custom_exception_hierarchy_and_message() {
        try {
            throw new AuthError("Authentication failed");
        } catch (AuthError e) {
            assertEquals("Authentication failed", e.getMessage());
            assertTrue(e instanceof AuthError);
            assertTrue(e instanceof SshAuditError);
        }

        try {
            throw new ConnectionError("Failed to connect");
        } catch (ConnectionError e) {
            assertEquals("Failed to connect", e.getMessage());
        }

        try {
            throw new ProtocolError("SSH protocol mismatch");
        } catch (ProtocolError e) {
            assertEquals("SSH protocol mismatch", e.getMessage());
        }
    }

    @Test
    public void test_ssh_audit_error_catch() {
        Exception[] exceptions = new Exception[]{
            new AuthError("auth err"),
            new ConnectionError("conn err"),
            new ProtocolError("proto err")
        };
        for (Exception e : exceptions) {
            try {
                throw e;
            } catch (SshAuditError err) {
                assertTrue(err.getMessage().endsWith("err"));
            } catch (Exception other) {
                fail("Should have caught SshAuditError");
            }
        }
    }
}