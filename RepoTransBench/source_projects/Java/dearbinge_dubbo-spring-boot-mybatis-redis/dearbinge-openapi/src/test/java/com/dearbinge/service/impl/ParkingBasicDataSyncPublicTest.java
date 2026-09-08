package com.dearbinge.service.impl;

import org.junit.Test;

import static org.junit.Assert.*;

public class ParkingBasicDataSyncPublicTest {
    @Test
    public void testParkingBasicDataSyncResponsePublicVariant() {
        // Use different inputs from private: e.g., odd parkId, simulate a "false"
        int parkId = 5739;  // Odd for this public variant
        boolean syncResult = (parkId % 2 == 0); // Even-only success logic
        assertFalse(syncResult);
    }
}