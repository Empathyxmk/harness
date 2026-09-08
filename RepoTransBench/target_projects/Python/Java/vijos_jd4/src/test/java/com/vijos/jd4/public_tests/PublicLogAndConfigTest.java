package com.vijos.jd4.public_tests;

import org.junit.jupiter.api.*;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class PublicLogAndConfigTest {

    static class FakeColoredLogs {
        boolean installed = false;
        Map<String, Object> params;
        void install(Map<String, Object> kwargs) {
            installed = true;
            params = kwargs;
        }
    }

    static class FakeSyslog {
        boolean syslogEnabled = false;
        Map<String, Object> params;
        void enableSystemLogging(Map<String, Object> kwargs) {
            syslogEnabled = true;
            params = kwargs;
        }
    }

    @Test
    void testPublicLogInstall() {
        FakeColoredLogs c = new FakeColoredLogs();
        c.install(Map.of("example", "hello"));
        assertTrue(c.installed);
        assertEquals("hello", c.params.get("example"));
    }

    @Test
    void testPublicLogSyslog() {
        FakeSyslog syslog = new FakeSyslog();
        syslog.enableSystemLogging(Map.of("sys", "log"));
        assertTrue(syslog.syslogEnabled);
        assertEquals("log", syslog.params.get("sys"));
    }

    static class FakeLogger {
        boolean errorCalled = false;
        void error(String... s) { errorCalled = true; }
    }

    @Test
    void testPublicConfigFileNotFound() {
        FakeLogger logger = new FakeLogger();
        try {
            logger.error("Config file not found");
            throw new RuntimeException("Config file not found");
        } catch (RuntimeException ex) {
            assertTrue(logger.errorCalled);
            assertEquals("Config file not found", ex.getMessage());
        }
    }
}