package com.packtpublishing.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.Map;
import java.util.HashMap;

class OriginalTestFlightStatusTest {

    // Simulate flight status
    Map<String, String> flightStatuses = new HashMap<>();

    OriginalTestFlightStatusTest() {
        flightStatuses.put("AB123", "on time");
        flightStatuses.put("BA456", "delayed");
    }

    String getStatus(String flightNo) {
        return flightStatuses.getOrDefault(flightNo, "unknown");
    }

    @Test
    void testFlightOnTime() {
        assertEquals("on time", getStatus("AB123"));
    }

    @Test
    void testFlightDelayed() {
        assertEquals("delayed", getStatus("BA456"));
    }

    @Test
    void testFlightUnknown() {
        assertEquals("unknown", getStatus("XX999"));
    }
}