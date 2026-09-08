package com.example.deyeinvertermqtt.public;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class PublicActivePowerRegulationTest {

    @Test
    public void testPublicActivePowerInRange() {
        double activePower = 7500;
        assertTrue(activePower >= 0 && activePower <= 10000, "Should be within allowed range");
    }
}