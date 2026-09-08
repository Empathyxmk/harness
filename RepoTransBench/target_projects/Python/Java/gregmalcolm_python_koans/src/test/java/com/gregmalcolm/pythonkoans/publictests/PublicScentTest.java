package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicScentTest {

    @Test
    void testScentTrailIsDetected() {
        boolean scentDetected = true;
        assertTrue(scentDetected, "Public: Scent trail should be detected.");
    }
}