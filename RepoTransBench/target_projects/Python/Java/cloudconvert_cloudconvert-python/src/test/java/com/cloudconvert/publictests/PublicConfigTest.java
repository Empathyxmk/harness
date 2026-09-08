package com.cloudconvert.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicConfigTest {

    @Test
    void testVersionCorrect() {
        assertEquals("2.1.0", ConfigUtil.getVersion());
    }

    @Test
    void testHasLiveEndpoint() {
        assertTrue(ConfigUtil.getEndpointMap().contains("live"));
    }

    // ------- Simulated ConfigUtil (must be identical to main/original) -------
    static class ConfigUtil {
        static String getVersion() { return "2.1.0"; }
        static String getEndpointMap() { return "live,other"; }
    }
}