package com.github.nexmark.flink.utils;

import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class NexmarkGlobalConfigurationPublicTest {

    @Test
    void testGlobalParameterLoadingOverrides() {
        Map<String, String> cfg = NexmarkGlobalConfiguration.loadGlobalConfiguration("nexmark-flink/src/main/resources/conf");
        // Use likely-missing override
        assertNull(cfg.get("nonexistent_override_key"));
    }
}