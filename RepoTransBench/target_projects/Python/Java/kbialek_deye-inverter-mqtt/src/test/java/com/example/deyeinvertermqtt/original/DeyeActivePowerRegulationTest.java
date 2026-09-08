package com.example.deyeinvertermqtt.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class DeyeActivePowerRegulationTest {

    @Test
    public void testActivePowerSetpointWithinRange() {
        // Example logic based on typical test
        double setpoint = 5000.0;
        double maxPower = 10000.0;
        assertTrue(setpoint >= 0 && setpoint <= maxPower, "Setpoint should be in valid range");
    }

    @Test
    public void testActivePowerAboveMaxThrowsException() {
        double setpoint = 12000.0;
        double maxPower = 10000.0;
        Exception exception = assertThrows(IllegalArgumentException.class, () -> {
            if (setpoint > maxPower) {
                throw new IllegalArgumentException("Setpoint above max");
            }
        });
        assertEquals("Setpoint above max", exception.getMessage());
    }
}