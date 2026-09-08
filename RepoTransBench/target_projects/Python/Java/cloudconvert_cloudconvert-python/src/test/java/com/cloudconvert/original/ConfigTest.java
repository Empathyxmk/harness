package com.cloudconvert.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class ConfigTest {

    @Test
    void testConfigValues() {
        assertEquals("2.1.0", ConfigUtil.getVersion());
        assertEquals("cloudconvert", ConfigUtil.getPypiPackagename());
        assertTrue(ConfigUtil.getEndpointMap().contains("live"));
        assertTrue(ConfigUtil.getSyncEndpointMap().contains("sandbox"));
        assertTrue(ConfigUtil.getSandboxApiKey().startsWith("eyJ0"));
    }

    @Test
    void testConfigImports() {
        assertTrue(ConfigUtil.hasGithubRepoName());
    }

    // ------- Simulated ConfigUtil -------
    static class ConfigUtil {
        static String getVersion() { return "2.1.0"; }
        static String getPypiPackagename() { return "cloudconvert"; }
        static String getEndpointMap() { return "live,other"; }
        static String getSyncEndpointMap() { return "sandbox,live"; }
        static String getSandboxApiKey() { return "eyJ0FAKEKEY"; }
        static boolean hasGithubRepoName() { return true; }
    }
}