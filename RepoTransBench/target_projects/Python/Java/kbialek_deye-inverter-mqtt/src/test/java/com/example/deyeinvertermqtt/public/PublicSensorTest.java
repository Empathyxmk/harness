package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicSensorTest {

    @Test
    public void testSensorReadingPositive() {
        int sensor = 10;
        assertTrue(sensor > 0, "Sensor reading should be positive");
    }
}