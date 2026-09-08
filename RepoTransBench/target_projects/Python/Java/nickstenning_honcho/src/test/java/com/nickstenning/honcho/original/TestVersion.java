package com.nickstenning.honcho.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestVersion {

    @Test
    void testVersionStringFormat() {
        String version = com.nickstenning.honcho.HonchoVersion.VERSION;
        assertNotNull(version);
        assertTrue(version.matches("\\d+\\.\\d+(\\.\\d+)?"));
    }
}