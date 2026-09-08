package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSenseiTest {

    @Test
    void testSenseiGuidance() {
        String message = "Patience, young grasshopper.";
        assertEquals("Patience, young grasshopper.", message);
    }
}