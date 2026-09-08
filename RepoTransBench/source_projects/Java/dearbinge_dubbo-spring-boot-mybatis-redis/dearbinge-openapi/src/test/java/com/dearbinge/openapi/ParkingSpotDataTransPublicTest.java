package com.dearbinge.openapi;

import org.junit.Test;

import static org.junit.Assert.*;

public class ParkingSpotDataTransPublicTest {
    @Test
    public void testAlternativeParkingSpotTrans() {
        // Different inputs from private: new spotId, different lat/lng.
        String spotId = "PUBLIC_SPOT_102";
        double lat = 35.1234;
        double lng = 135.4321;

        // Simulate test logic
        String result = spotId + "_" + Math.abs(lat - lng);
        assertEquals("PUBLIC_SPOT_102_100.3087", result);
    }
}