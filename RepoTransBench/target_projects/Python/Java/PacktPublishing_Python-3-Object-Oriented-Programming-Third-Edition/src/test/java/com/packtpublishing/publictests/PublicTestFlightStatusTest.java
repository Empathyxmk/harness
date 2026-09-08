package com.packtpublishing.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import java.util.Map;
import java.util.HashMap;

class PublicTestFlightStatusTest {
    private static final Map<String, String> flightStatuses = new HashMap<>();
    static {
        flightStatuses.put("FL123", "on time");
        flightStatuses.put("FL234", "cancelled");
    }

    static String getStatus(String flightNo) {
        return flightStatuses.getOrDefault(flightNo, "unknown");
    }

    @Test
    void testStatusOnTime() {
        assertEquals("on time", getStatus("FL123"));
    }

    @Test
    void testStatusCancelled() {
        assertEquals("cancelled", getStatus("FL234"));
    }

    @Test
    void testStatusUnknown() {
        assertEquals("unknown", getStatus("XZ999"));
    }
}