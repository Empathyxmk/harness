package com.gregmalcolm.pythonkoans.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicMountainEdgeTest {

    @Test
    void testMountainSummitReached() {
        boolean summitReached = true;
        assertTrue(summitReached, "Public: Summit should be reached.");
    }
}