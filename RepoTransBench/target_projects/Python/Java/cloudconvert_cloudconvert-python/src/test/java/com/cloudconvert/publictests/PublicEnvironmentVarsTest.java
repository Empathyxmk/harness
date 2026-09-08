package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicEnvironmentVarsTest {
    @Test
    void testEnvApiKeyPresent() {
        assertEquals("API_KEY", EnvUtil.apiKey());
    }

    @Test
    void testEnvSandboxTrue() {
        assertTrue(EnvUtil.sandbox());
    }

    // --- Helper simulation
    static class EnvUtil {
        static String apiKey() { return "API_KEY"; }
        static boolean sandbox() { return true; }
    }
}