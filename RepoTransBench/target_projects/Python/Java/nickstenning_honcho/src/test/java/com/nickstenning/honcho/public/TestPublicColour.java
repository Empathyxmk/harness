package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicColour {

    @Test
    void testBoldColourIsDefined() {
        assertNotNull(com.nickstenning.honcho.HonchoColour.BOLD);
    }

    @Test
    void testResetColourIsDefined() {
        assertNotNull(com.nickstenning.honcho.HonchoColour.RESET);
    }
}