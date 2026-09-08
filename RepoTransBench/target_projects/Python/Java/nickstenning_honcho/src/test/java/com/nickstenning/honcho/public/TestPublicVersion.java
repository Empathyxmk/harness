package com.nickstenning.honcho.public_;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestPublicVersion {

    @Test
    void testVersionIsDefined() {
        String version = com.nickstenning.honcho.HonchoVersion.VERSION;
        assertNotNull(version);
        assertFalse(version.isEmpty());
    }
}