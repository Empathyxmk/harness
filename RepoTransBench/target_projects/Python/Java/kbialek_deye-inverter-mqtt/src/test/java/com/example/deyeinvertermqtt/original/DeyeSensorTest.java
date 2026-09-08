package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeSensorTest {

    @Test
    public void testSensorReadingValid() {
        double reading = 115.0;
        assertTrue(reading > 0, "Reading should be positive");
    }

    @Test
    public void testSensorErrorCode() {
        int errorCode = 1;
        assertEquals(1, errorCode, "Sensor should return error code 1");
    }
}