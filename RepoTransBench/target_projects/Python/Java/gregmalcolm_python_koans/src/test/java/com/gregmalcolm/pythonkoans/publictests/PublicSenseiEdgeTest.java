package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicSenseiEdgeTest {

    @Test
    void testSenseiEncouragement() {
        String encouragement = "You are doing well.";
        assertEquals("You are doing well.", encouragement);
    }
}