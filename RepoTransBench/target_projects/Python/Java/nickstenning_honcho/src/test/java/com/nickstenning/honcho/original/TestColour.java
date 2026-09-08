package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestColour {

    @Test
    void testColourCodes() {
        // Simulate colour code reset or basic semantic mapping, assuming your HonchoColour class
        assertEquals("\033[0m", com.nickstenning.honcho.HonchoColour.RESET);
        assertEquals("\033[1m", com.nickstenning.honcho.HonchoColour.BOLD);
    }
}